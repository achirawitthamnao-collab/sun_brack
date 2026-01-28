import discord
from discord.ext import commands
import os
import re
import google.generativeai as genai

# 👇 เรียกใช้ฟังก์ชันเปิด Server จากไฟล์ myserver.py (เหมือนเดิม)
from myserver import server_on

# =====================
# ENV SETUP
# =====================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # 👈 เปลี่ยนชื่อตัวแปรให้ตรงกับ Gemini

# =====================
# GEMINI SETUP
# =====================
# ตั้งค่า API Key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("❌ Warning: ไม่พบ GEMINI_API_KEY")

# ตั้งค่า Model และ System Instruction (บุคลิกบอท)
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="คุณคือบอท Discord ภาษาไทย พูดจาเป็นกันเอง สุภาพ กวนนิดๆ ได้แต่ห้ามหยาบคาย ตอบสั้นกระชับ ไม่ต้องยาวมาก"
)

# =====================
# BOT SETUP
# =====================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================
# BAD WORDS
# =====================
bad_words = [
    "ควย", "เหี้ย", "สันดาน", "หี",
    "หรรม", "หำ", "โง่", "กาก", "กระจอก"
]

# =====================
# FUNCTIONS
# =====================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

async def ask_gemini(text: str) -> str:
    try:
        # ส่งข้อความไปหา Gemini (ใช้ async เพื่อไม่ให้บอทค้าง)
        response = await model.generate_content_async(text)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "ตอนนี้สมองเบลอ ขอพักแป๊บ 😵‍💫 (Error จาก Google)"

# =====================
# EVENTS
# =====================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"✅ Gemini Key: {'OK' if GEMINI_API_KEY else 'MISSING'}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ถ้าเป็นคำสั่ง "!" ให้ทำงานคำสั่ง
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    raw = message.content
    content = clean_text(raw)

    # 1. เช็คคำหยาบ
    for w in bad_words:
        if w in content:
            await message.channel.send(f"พูดดี ๆ หน่อยนะ {message.author.mention} 😅")
            return

    # 2. ตอบ Keyword
    if content.startswith("สวัสดี"):
        await message.channel.send(f"สวัสดีครับ {message.author.mention} 👋")
    
    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้า {message.author.mention} 😄")
        
    elif "ใครคือsun" in content:
        await message.channel.send(f"ก็คุณไง 😎 {message.author.mention}")

    # 3. ให้ Gemini ตอบ (ถ้าไม่เข้าเงื่อนไขบน)
    else:
        async with message.channel.typing():
            reply = await ask_gemini(raw)
            # ตัดคำถ้าเกิน 1900 ตัวอักษร
            if len(reply) > 1900: reply = reply[:1900] + "..."
            await message.channel.send(f"{reply} {message.author.mention}")

# =====================
# MAIN RUN
# =====================
if __name__ == "__main__":
    if DISCORD_TOKEN:
        server_on()
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ Error: ไม่พบ DISCORD_TOKEN")
