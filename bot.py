import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

# ===== 1. LOAD ENV & CONFIG =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== 2. INTENTS =====
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก: ต้องเปิดใน Discord Developer Portal ด้วย
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== 3. BAD WORDS LIST =====
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

# ===== 4. CLEAN TEXT FUNCTION =====
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)  # ลบช่องว่าง
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)  # ลบอักขระพิเศษ
    return text

# ===== 5. EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")

@bot.event
async def on_message(message):
    # ป้องกันบอทตอบโต้ตัวเอง
    if message.author.bot:
        return

    # เตรียมข้อความสำหรับการเช็ค
    raw_content = message.content.strip()
    clean_content = clean_text(raw_content)

    # --- ส่วนที่ 1: ระบบลบคำไม่สุภาพ ---
    for word in bad_words:
        if word in clean_content:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention} ใช้คำสุภาพหน่อยน้า", delete_after=5)
            except Exception as e:
                print(f"❌ ไม่สามารถลบข้อความได้ (ขาด Permission): {e}")
            return # หยุดการทำงานทันทีถ้าเจอคำหยาบ

    # --- ส่วนที่ 2: ระบบส่งโค้ด (PHP, CSS, HTML) ---
    keywords = ["php", "css", "html", "โค้ด"]
    
    # เช็คว่ามี keyword ใดอยู่ในข้อความหรือไม่
    if any(x in clean_content for x in keywords):
        
        # ส่งโค้ด PHP
        if "php" in clean_content or "โค้ด" in clean_content:
            php_code = "```php\n<?php\n$name=trim($_POST['name']);\n$file='data.txt';\n$f=fopen($file,'a');\nfwrite($f, $name.\"\\n\");\nfclose($f);\n?>\n```"
            await message.channel.send(f"**PHP Code Example:**\n{php_code}")

        # ส่งโค้ด CSS
        if "css" in clean_content or "โค้ด" in clean_content:
            css_code = "```css\nbody {\n  font-family: 'Prompt', sans-serif;\n  background: #f0f0f0;\n  display: flex;\n  justify-content: center;\n}\n```"
            await message.channel.send(f"**CSS Code Example:**\n{css_code}")

        # ส่งโค้ด HTML
        if "html" in clean_content or "โค้ด" in clean_content:
            html_code = "```html\n<!DOCTYPE html>\n<html>\n<head><title>Page</title></head>\n<body>\n  <form method='post' action='save.php'>\n    <input type='text' name='name'>\n    <button type='submit'>Send</button>\n  </form>\n</body>\n</html>\n```"
            await message.channel.send(f"**HTML Code Example:**\n{html_code}")

        return  # หยุดการทำงานเพื่อไม่ให้ซ้ำซ้อน

    # --- ส่วนที่ 3: ประมวลผลคำสั่ง Prefix (!...) ---
    await bot.process_commands(message)

# ===== 6. RUN BOT =====
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ ไม่พบ DISCORD_TOKEN ในไฟล์ .env")
