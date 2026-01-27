import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

from myserver import server_on

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== BAD WORDS =====
bad_words = [
    "ควย", "เหี้ย", "สันดาน", "หี",
    "หรรม", "หำ", "โง่", "กาก", "กระจอก"
]

# ===== CLEAN TEXT =====
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

# ===== BOT READY =====
@bot.event
async def on_ready():
    print("Bot is ready!")

# ===== RESPONSES (INTENT SYSTEM) =====
responses = [
    {"keys": ["สวัสดี", "สวัดดี", "hello", "hi"], "reply": "สวัสดีจ้า"},
    {"keys": ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"], "reply": "ดีจ้า"},
    {"keys": ["ไม่รู้"], "reply": "ทำไมถึงไม่รู้ล่ะ"},
    {"keys": ["ใครคือsun", "sunคือใคร"], "reply": "เราเองไง 😆"},
    {"keys": ["คิดเหมือน"], "reply": "ใช่เลย คิดเหมือนกัน"},
    {"keys": ["ไม่ชอบ", "เกลียด"], "reply": "เราก็ไม่ค่อยชอบเหมือนกัน"},
    {"keys": ["ทำอะไรได้", "ทำไรได้"], "reply": "ทำได้หลายอย่างเลยนะ"},
    {"keys": ["กลัว"], "reply": "ไม่ต้องกลัวนะ เราอยู่นี่"},
    {"keys": ["ฝันดี", "นอน", "นอนล่ะ", "จะนอน"], "reply": "ฝันดีนะ 😴"},
    {"keys": ["ฮึ่ย", "เฮ้อ"], "reply": "เป็นอะไรหรือเปล่า"},
    {"keys": ["เปล่า", "ป่าว"], "reply": "โอเค โล่งใจไปที"},
    {"keys": ["ทำไร", "ทำอะไร"], "reply": "กำลังนั่งคุยอยู่นี่แหละ"},
    {"keys": ["sun"], "reply": "เราเอง ๆ แสงสว่างท่ามกลางความมืด ✨"}
]

# ===== MESSAGE EVENT =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content
    content = clean_text(raw)

    # ----- FILTER BAD WORD -----
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(
                f"{message.author.mention} กรุณาใช้คำสุภาพนะ"
            )
            return

    # ----- AUTO RESPONSE -----
    answered = False

    for item in responses:
        for key in item["keys"]:
            if key in content:
                await message.channel.send(
                    f"{item['reply']} {message.author.mention}"
                )
                answered = True
                break
        if answered:
            break

    # ----- FALLBACK -----
    if not answered:
        await message.channel.send(
            f"เรายังไม่ค่อยเข้าใจ แต่เล่าต่อได้นะ {message.author.mention}"
        )

    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
