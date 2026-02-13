import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CONFIGURATION =====
# รายชื่อคำหยาบ
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

# ฟังก์ชันทำความสะอาดข้อความเพื่อเช็คคำหยาบ
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")

@bot.event
async def on_message(message):
    # ไม่ตอบโต้กับบอทด้วยกันเอง
    if message.author.bot:
        return

    content_raw = message.content.strip()
    content_clean = clean_text(content_raw)

    # --- 1. ระบบตรวจจับและลบคำหยาบ ---
    for word in bad_words:
        if word in content_clean:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention} ใช้คำสุภาพหน่อยน้า (ข้อความนี้จะถูกลบใน 5 วิ)", delete_after=5)
            except discord.Forbidden:
                print("❌ บอทไม่มีสิทธิ์ลบข้อความ (Permissions Error)")
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")
            return # เจอคำหยาบแล้วหยุดทำงานส่วนอื่นทันที

    # --- 2. ระบบแจกโค้ด ---
    # เช็คว่ามีคำสำคัญในข้อความหรือไม่
    keywords = ["โค้ด", "php", "html", "css"]
    if any(key in content_clean for key in keywords):
        
        # ส่งโค้ด PHP
        if "php" in content_clean or "โค้ด" in content_clean:
            php_code = "```php\n<?php\n$name = trim($_POST['name']);\n$file = 'data.txt';\n$f = fopen($file, 'a');\nfwrite($f, $name . \"\\n\");\nfclose($f);\necho 'บันทึกสำเร็จ!';\n?>\n```"
            await message.channel.send(f"📂 **ตัวอย่าง PHP Code:**\n{php_code}")

        # ส่งโค้ด CSS
        if "css" in content_clean or "โค้ด" in content_clean:
            css_code = "```css\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody {\n  font-family: 'Prompt', sans-serif;\n  background-color: #f4f4f4;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 100vh;\n}\n```"
            await message.channel.send(f"🎨 **ตัวอย่าง CSS Code:**\n{css_code}")

        # ส่งโค้ด HTML
        if "html" in content_clean or "โค้ด" in content_clean:
            html_code = "```html\n<!DOCTYPE html>\n<html>\n<head>\n  <title>My Page</title>\n</head>\n<body>\n  <form method='post' action='save.php'>\n    <input type='text' name='name' placeholder='ใส่ชื่อที่นี่'>\n    <button type='submit'>ส่งข้อมูล</button>\n  </form>\n</body>\n</html>\n```"
            await message.channel.send(f"🌐 **ตัวอย่าง HTML Code:**\n{html_code}")

    # ให้คำสั่ง prefix (ถ้ามี) ทำงานปกติ
    await bot.process_commands(message)

# ===== RUN =====
bot.run(TOKEN)
