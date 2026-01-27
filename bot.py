import discord
from discord.ext import commands
import os
import re
import random
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

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # =====================
    # 1️⃣ BAD WORD CHECK
    # =====================
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(
                f"{message.author.mention} ใช้คำสุภาพหน่อยน้า",
                delete_after=5
            )
            return

    # =====================
    # 2️⃣ ตัวอักษรล้วน ก-ฮ / a-z
    # =====================
    if re.fullmatch(r"[ก-ฮ]", raw):
        await message.channel.send(f"พิมพ์ตัวเดียวเองหรอ {message.author.mention}")
        return

    elif re.fullmatch(r"[ก-ฮ]+", raw):
        await message.channel.send(f"อักษรไทยล้วนเลยนะ {message.author.mention}")
        return

    elif re.fullmatch(r"[a-zA-Z]+", raw):
        await message.channel.send(f"อังกฤษล้วนเลยแฮะ {message.author.mention}")
        return

    # =====================
    # 3️⃣ KEYWORDS
    # =====================
    if content.startswith("สวัสดี"):
        await message.channel.send(f"สวัสดี {message.author.mention}")

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้า {message.author.mention}")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention}")

    elif "ไม่รู้" in content:
        await message.channel.send(f"ทำไมไม่รู้ {message.author.mention}")

    elif "ใครคือsun" in content or "sunคือใคร" in content:
        await message.channel.send(f"เราไง {message.author.mention}")

    elif "ไม่ชอบ" in content:
        await message.channel.send(f"เราก็ไม่ชอบ {message.author.mention}")

    elif "ทำไรได้" in content or "ทำอะไรได้" in content:
        await message.channel.send(f"ทำได้หลายอย่างเลย {message.author.mention}")

    elif "กลัว" in content:
        await message.channel.send(f"ไม่ต้องกลัวนะ {message.author.mention}")

    elif "ฝันดี" in content or "นอน" in content:
        await message.channel.send(f"ฝันดีนะ {message.author.mention}")

    elif "ทำไร" in content:
        await message.channel.send(f"นอนอยู่ {message.author.mention}")

    elif "?" in raw or raw.endswith("ไหม") or raw.endswith("หรอ"):
        await message.channel.send(
            f"คำถามน่าสนใจนะ แล้วคุณคิดว่ายังไงล่ะ {message.author.mention}"
        )

    # =====================
    # 5️⃣ FALLBACK (ถามอะไรก็ตอบได้)
    # =====================
    else:
        fallback = [
            "อืมม 🤔",
            "เล่าต่อสิ",
            "น่าสนใจนะ",
            "5555",
            "โอเคเลย",
            "ฟังอยู่นะ",
            "เข้าใจละ"
        ]
        await message.channel.send(
            f"{random.choice(fallback)} {message.author.mention}"
        )

    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
