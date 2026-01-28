import discord
from discord.ext import commands
import os
import re
from openai import OpenAI

# 👇 นำเข้าฟังก์ชัน server_on จากไฟล์ myserver.py
from myserver import server_on

# =====================
# ENV FROM DASHBOARD
# =====================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =====================
# OPENAI CLIENT
# =====================
client = OpenAI()

# =====================
# INTENTS
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
# CLEAN TEXT
# =====================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

# =====================
# ASK AI (FALLBACK)
# =====================
async def ask_ai(text: str) -> str:
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "คุณคือบอท Discord ภาษาไทย "
                        "พูดเป็นกันเอง สุภาพ ตอบตรงคำถาม "
                        "ตอบสั้น กระชับ ห้ามใช้คำหยาบ"
                    )
                },
                {"role": "user", "content": text}
            ],
            temperature=0.7,
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print("AI ERROR:", e)
        return "ตอนนี้สมองเบลอ ขอพักแป๊บ 😵‍💫"

# =====================
# EVENTS
# =====================
@bot.event
async def on_ready():
    print("---------------------------------")
    print("DISCORD_TOKEN:", "OK" if DISCORD_TOKEN else "MISSING")
    print("OPENAI_API_KEY:", "OK" if OPENAI_API_KEY else "MISSING")
    print(f"🤖 Logged in as {bot.user}")
    print("---------------------------------")

@bot.event
async def on_message(message):
    # 1. ข้ามถ้าเป็นบอท
    if message.author.bot:
        return

    # 2. ถ้าเป็นคำสั่ง prefix "!" ให้ข้ามไปทำงานส่วนคำสั่งเลย
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    raw = message.content
    content = clean_text(raw)

    # 3. ตรวจคำหยาบ
    for w in bad_words:
        if w in content:
            await message.channel.send(f"พูดดี ๆ หน่อยนะ {message.author.mention} 😅")
            return

    # 4. ตอบตาม Keyword
    if content.startswith("สวัสดี"):
        await message.channel.send(f"สวัสดี {message.author.mention} 👋")

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้าา {message.author.mention} 😄")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention} 👋")

    elif "ใครคือsun" in content:
        await message.channel.send(f"ก็คุณไง 😎 {message.author.mention}")

    elif "ไม่รู้" in content:
        await message.channel.send(f"ไม่รู้จริงเหรอ 🤔 {message.author.mention}")

    # 5. ถ้าไม่ตรง Keyword ให้ถาม AI
    else:
        async with message.channel.typing():
            ai_reply = await ask_ai(raw)
            # ตัดคำถ้าเกิน 1900 ตัวอักษร
            if len(ai_reply) > 1900:
                ai_reply = ai_reply[:1900] + "..."
            
            await message.channel.send(f"{ai_reply} {message.author.mention}")

# =====================
# RUN
# =====================
if __name__ == "__main__":
    if DISCORD_TOKEN:
        # เปิด Server ก่อนรันบอท
        server_on()
        bot.run(DISCORD_TOKEN)
    else:
        print("❌ Error: ไม่พบ DISCORD_TOKEN ใน Environment Variables")
