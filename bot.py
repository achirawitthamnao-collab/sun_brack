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
    text = re.sub(r"\s+", "", text)            # ลบช่องว่าง
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)   # ลบอักขระแปลก
    return text

# ===== READY =====
@bot.event
async def on_ready():
    print("Bot is ready!")

# ===== MESSAGE EVENT =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content
    content = clean_text(raw)

    # ---------- FILTER BAD WORD ----------
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

    # ---------- RESPONSES ----------
    if content.startswith("สวัสดี"):
        await message.channel.send(f"สวัสดี {message.author.mention}")

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้า {message.author.mention}")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention}")

    elif content in ["ไร", "อะไร"]:
        await message.channel.send(f"ไม่รู้เหมือนกัน {message.author.mention}")

    elif "ไม่รู้" in content:
        await message.channel.send(f"ทำไมไม่รู้ {message.author.mention}")

    elif "ใครคือsun" in content:
        await message.channel.send(f"เราไง {message.author.mention}")

    elif "คิดเหมือน" in content:
        await message.channel.send(f"ใช่ คิดเหมือนกัน {message.author.mention}")

    elif "ไม่ชอบ" in content:
        await message.channel.send(f"เราก็ไม่ชอบ {message.author.mention}")

    elif "ทำไรได้" in content or "ทำอะไรได้" in content:
        await message.channel.send(f"ทำได้หลายอย่างเลย {message.author.mention}")

    elif "กลัว" in content:
        await message.channel.send(f"ไม่ต้องกลัวนะ {message.author.mention}")

    elif content in ["ใจ", "จัย"]:
        await message.channel.send(f"ไม่สนใจแล้ว {message.author.mention}")

    elif "ฝันดี" in content or "นอน" in content:
        await message.channel.send(f"ฝันดีนะ {message.author.mention}")

    elif "ฮึ่ย" in content:
        await message.channel.send(f"เป็นอะไรหรอ {message.author.mention}")

    elif "เปล่า" in content or "ป่าว" in content:
        await message.channel.send(f"ดีแล้วที่ไม่เป็นไร {message.author.mention}")

    elif "sun" in content:
        await message.channel.send(
            f"เราเองๆ เป็นแสงสว่างท่ามกลางความมืด! {message.author.mention}"
        )

    elif content in ["ส", "สว", "สวั", "สวัส", "สวัสด"]:
        await message.channel.send(f"สวัสดีใช่ไหม {message.author.mention}")

    elif content.startswith(("ค", "คว")):
        try:
            await message.delete()
        except:
            pass
        await message.channel.send(f"ไม่ได้ๆ {message.author.mention}")
    else:
        await message.channel.send(f"ไม่เข้าใจ {message.author.mention}")

    # ให้คำสั่ง bot ทำงานได้
    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
