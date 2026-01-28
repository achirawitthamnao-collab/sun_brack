# ไฟล์: bot.py
import discord
from discord.ext import commands
import os
import re
import random
from dotenv import load_dotenv
import google.generativeai as genai
from myserver import server_on  # <--- เรียกใช้ไฟล์ server ที่เราสร้าง

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ===== SETUP AI (GEMINI) =====
# ใช้ try-except เผื่อใครยังไม่ได้ใส่ Key จะได้ไม่แครช
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("⚠️ Warning: ไม่พบ GEMINI_API_KEY บอทจะตอบได้แค่คำถามทั่วไป")
    model = None

ai_persona = """
คุณคือ "BotKub" (บอทครับ) เพื่อนคู่คิดใน Discord
นิสัย: กวนตีนนิดๆ, เป็นกันเอง, ใช้ภาษาวัยรุ่น
ความสามารถพิเศษ: เก่งการเขียนโปรแกรมมาก (Python, JS, C++)
หน้าที่:
1. ถ้าเขาถามเรื่องโค้ด: สอนแบบเข้าใจง่าย ยกตัวอย่างประกอบ
2. ถ้าเขาคุยเล่น: คุยกลับแบบเพื่อนสนิท
"""

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DATA =====
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

brain = [
    {"tags": ["ดีครับ", "สวัสดี", "หวัดดี", "hi", "hello"], "answers": ["โย่ววว ว่าไงวัยรุ่น", "ดีจ้า วันนี้เขียนโค้ดบ้างยัง?", "มาแล้วครับผม"]},
    {"tags": ["ขอบคุณ", "thx", "แต้ง"], "answers": ["ไม่เป็นไร เพื่อนกัน", "เลี้ยงกาแฟแก้วนึงพอ", "ยินดีครับผม"]},
    {"tags": ["555", "ตลก", "ขำ"], "answers": ["ขำไรอะ แบ่งมั่ง", "เส้นตื้นนะเรา", "555555"]},
    {"tags": ["ชื่อไร", "ชื่ออะไร"], "answers": ["ชื่อ BotKub สุดหล่อไงครับ", "เรียกพี่บอทก็ได้น้อง"]}
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw_content = message.content.strip()
    clean_content = clean_text(raw_content)

    # 1. เช็คคำหยาบ
    if any(word in raw_content for word in bad_words):
        try: await message.delete()
        except: pass
        await message.channel.send(f"{message.author.mention} อย่าหยาบคายดิครับ!", delete_after=5)
        return

    # 2. เช็คสมองส่วนหน้า (คำตอบตายตัว)
    for item in brain:
        for tag in item["tags"]:
            if tag in clean_content:
                await message.channel.send(f"{random.choice(item['answers'])} {message.author.mention}")
                return

    # 3. ส่งให้ AI (สอนโค้ด/คุยทั่วไป)
    if model and len(raw_content) > 1:
        async with message.channel.typing():
            try:
                prompt = f"{ai_persona}\n\nUser: {raw_content}"
                response = model.generate_content(prompt)
                await message.channel.send(response.text)
            except Exception as e:
                print(f"AI Error: {e}")
                await message.channel.send("โทษที สมองเออเร่อนิดหน่อย ถามใหม่ซิ")
                
    await bot.process_commands(message)

# ===== START =====
if __name__ == "__main__":
    server_on() # <--- เปิด Server หลอก Render
    bot.run(TOKEN)
