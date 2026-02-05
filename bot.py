แบบนี้หรอimport discord
from discord.ext import commands
import os
import re
import random
import sqlite3  # เพิ่มระบบฐานข้อมูล
from dotenv import load_dotenv
from myserver import server_on

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== DATABASE SETUP =====
# สร้างไฟล์ database.db ถ้ายังไม่มี
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    key_clean TEXT PRIMARY KEY,
    key_raw TEXT,
    value TEXT
)
""")
db.commit()

# ฟังก์ชันโหลดข้อมูลจาก DB มาเก็บใน memory เพื่อให้บอทตอบไวขึ้น
def load_custom_responses():
    cursor.execute("SELECT key_clean, value FROM responses")
    return dict(cursor.fetchall())

custom_responses = load_custom_responses()

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== BAD WORDS =====
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

# ===== CLEAN TEXT =====
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # 1. BAD WORD CHECK
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(f"{message.author.mention} ใช้คำสุภาพหน่อยน้า", delete_after=5)
            return

    # 2. TEACH BOT (ระบบจดจำลงฐานข้อมูล)
    if raw.startswith("ต้องตอบแบบนี้"):
        try:
            data = raw.replace("ต้องตอบแบบนี้", "").strip()
            key, value = data.split("|", 1)
            key_clean = clean_text(key)
            val_strip = value.strip()

            # บันทึกลง Database
            cursor.execute(
                "INSERT OR REPLACE INTO responses (key_clean, key_raw, value) VALUES (?, ?, ?)",
                (key_clean, key.strip(), val_strip)
            )
            db.commit()
            
            # อัปเดตตัวแปรในเครื่องทันที
            custom_responses[key_clean] = val_strip

            await message.reply(f"จำใส่สมองแล้วน้า 👍 ถ้าพิมพ์ว่า **{key.strip()}** จะตอบว่า\n> {val_strip}")
        except Exception as e:
            await message.reply("รูปแบบไม่ถูกน้า 😅 ลองใช้: `ต้องตอบแบบนี้ คำถาม|คำตอบ`")
        return

    # 3. CUSTOM RESPONSES (ดึงจาก DB มาตอบ)
    if content in custom_responses:
        await message.reply(custom_responses[content])
        return

    # 4. RANDOM LETTER CHECK
    if re.fullmatch(r"[ก-ฮa-zA-Z]", raw):
        await message.reply("จะรอพิมพ์น่ะ")
        return

    # 5. KEYWORDS CHAT (Hardcoded)
    if content.startswith("สวัสดี"):
        await message.reply("สวัสดีเป็นไงบ้างวันนี้~ มีอะไรอยากคุยเป็นพิเศษไหม")

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ", "hi", "hello"]:
        await message.reply("ดีจ้า/Hello")

    elif "คิดถึง" in content:
        await message.reply("คิดถึงเหมือนกันนะ 🌱 ช่วงนี้เป็นยังไงบ้าง เหนื่อยไหม เรานั่งฟังได้เสมอ 🙂")

    elif "cry" in content:
        await message.reply("เฮ้… 🫂 ถ้ามันหนักมากก็ร้องออกมาได้เลยนะ เราอยู่ตรงนี้เป็นเพื่อนเอง 💙")

    elif any(x in content for x in ["คิดยังไงกับเรา", "คิดยังไงกับฉัน"]):
        await message.reply("ผมมองว่านายเป็นคนที่พยายามและใจดีมากเลยนะ อย่าลืมใจดีกับตัวเองด้วยล่ะ")

    elif "ทำอะไรได้" in content or "ทำไรได้" in content:
        await message.reply("คุยเล่น เล่นมุก หรือจะให้เขียนโค้ดให้ก็ได้นะ")

    elif "ไม่รู้" in content:
        await message.reply("ไม่รู้ไม่เป็นไร แค่มีนายมานั่งคุยด้วยตรงนี้ก็ดีแล้ว")

    elif "เบื่อ" in content:
        await message.reply("เบื่อเหรอ? ลองคุยเรื่องมุกกากๆ หาเกมเล่น หรือจะระบายให้เราฟังก็ได้นะ")

    elif content in ["ไง", "ว่าไง", "งาย", "ว่างาย"]:
        await message.reply("ว่าไง~ สบายดีไหมวันนี้")

    elif any(x in content for x in ["ไม่ชอบเรา", "รำคาญ", "ไล่เรา"]):
        await message.reply("ไม่เคยรำคาญเลยนะ สบายใจได้ เรายินดีที่มีนายอยู่ตรงนี้เสมอ 😊")

    elif "ไหว" in content:
        await message.reply("ที่บอกว่า 'ยังไหว' น่ะ เก่งมากแล้วนะ แต่ถ้าไม่ไหวก็พักก่อนได้นะ")

    elif "ฝันดี" in content or "นอน" in content:
        await message.reply("ฝันดีน้าา ขอให้ตื่นมาพร้อมความสดใสครับ")

    # --- ส่วนส่งโค้ด (เปลี่ยนเป็น Reply) ---
    elif any(x in content for x in ["php", "css", "html", "โค้ด"]):
        if "php" in content or "โค้ด" in content:
            await message.reply("```php\n<?php\n// โค้ด PHP ของคุณ\n?>\n```")
        if "css" in content or "โค้ด" in content:
            await message.reply("```css\n/* โค้ด CSS ของคุณ */\n```")
        if "html" in content or "โค้ด" in content:
            await message.reply("```html\n\n```")

    elif "?" in raw:
        await message.reply("สงสัยอะไรหรอ ถามได้นะ")

    else:
        fallback = ["อืม 🤔", "เล่าต่อสิ", "เข้าใจๆ", "โอเคเลย", "ฟังอยู่นะ", "ออเครๆ"]
        await message.reply(random.choice(fallback))

# ===== RUN =====
server_on()
bot.run(TOKEN)
