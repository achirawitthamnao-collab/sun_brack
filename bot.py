import discord
from discord.ext import commands
import os
import re

# ===== TOKEN SETUP =====
# พยายามดึงจาก Environment Variable ของ Render โดยตรง
TOKEN = os.environ.get("DISCORD_TOKEN")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CONFIGURATION =====
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

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
    if message.author.bot:
        return

    content_raw = message.content.strip()
    content_clean = clean_text(content_raw)

    # --- 1. ระบบลบคำหยาบ ---
    for word in bad_words:
        if word in content_clean:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention} ใช้คำสุภาพหน่อยน้า", delete_after=5)
            except:
                pass 
            return

    # --- 2. ระบบแจกโค้ด ---
    keywords = ["โค้ด", "php", "html", "css"]
    if any(key in content_clean for key in keywords):
        if "php" in content_clean or "โค้ด" in content_clean:
            await message.channel.send("📂 **PHP Code:**\n```php\n<?php echo 'Hello World'; ?>\n```")
        if "css" in content_clean or "โค้ด" in content_clean:
            await message.channel.send("🎨 **CSS Code:**\n```css\nbody { background: #f4f4f4; }\n```")
        if "html" in content_clean or "โค้ด" in content_clean:
            await message.channel.send("🌐 **HTML Code:**\n```html\n<h1>Hello</h1>\n```")

    await bot.process_commands(message)

# ===== START BOT =====
if __name__ == "__main__":
    if TOKEN:
        print("🚀 กำลังเริ่มการทำงานของบอท...")
        bot.run(TOKEN)
    else:
        # ถ้าขึ้นข้อความนี้ใน Log แสดงว่าใน Render ยังตั้งค่าไม่ถูก
        print("❌ FATAL ERROR: หา DISCORD_TOKEN ไม่พบใน Environment Variables!")
        print("กรุณาตรวจสอบหน้า Environment ใน Render ว่าสะกด 'DISCORD_TOKEN' ถูกต้องและไม่มีช่องว่าง")
