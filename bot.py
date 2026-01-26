import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

from myserver import server_on

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bad_words = [
    "ควย", "เหี้ย", "สันดาน", "หี",
    "หรรม", "หำ", "โง่", "กาก", "กระจอก"
]

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)            # ลบช่องว่าง
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)   # ลบตัวอักษรแปลก
    return text

@bot.event
async def on_ready():
    print("ok")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    raw = message.content
    content = clean_text(raw)

    # ตรวจคำหยาบ
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

    # ===== คำทักทาย =====
    if content.startswith("สวัสด"):
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

    # ถ้าไม่เข้าเงื่อนไข → เงียบ
    else:
        await message.channel.send(f"ไม่เข้าใจแฮะ {message.author.mention}")

server_on()
bot.run(TOKEN)



