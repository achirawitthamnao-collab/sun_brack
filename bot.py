import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from myserver import server_on  # ต้องมีไฟล์นี้จริง

# โหลด .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# คำหยาบ
bad_words = [
    "ควย", "เหี้ย", "สันดาน", "หี",
    "หรรม", "หำ", "โง่", "กาก", "กระจอก"
]

@bot.event
async def on_ready():
    print("ok")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # ตรวจคำหยาบ
    for word in bad_words:
        if word in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} กรุณาใช้คำสุภาพนะ (ตรวจพบคำว่า: {word})"
            )
            return

    # คำทักทาย
    if content in ["สวัสดี","ดี"]:
        await message.channel.send(f"สวัสดี {message.author.mention}")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention}")

    elif content in ["ส", "สว", "สวั", "สวัส", "สวัสด"]:
        await message.channel.send(f"สวัสดีใช่ไหม {message.author.mention}")

    elif content == "ไร":
        await message.channel.send(f"ไม่รู้เหมือนกัน {message.author.mention}")
    elif content == "มะรู้สิ":
        await message.channel.send(f"ทำไมไม่รู้ {message.author.mention}")
    elif content == "ใครคือ​sun":
        await message.channel.send(f"เราไง {message.author.mention}")
    elif content == "คิดเหมือนกัน":
        await message.channel.send(f"ใช่คิดเหมือนกาน {message.author.mention}")
    elif content == "ไม่ชอบ":
        await message.channel.send(f"เราก็ไม่ชอบ {message.author.mention}")
    elif content == "ทำไรได้":
        await message.channel.send(f"หลายท่าเลย {message.author.mention}")
    elif content == "ดูมัน":
        await message.channel.send(f"มันเผาหรอ {message.author.mention}")
    elif content == "กลัว":
        await message.channel.send(f"โอ๋ๆไม่ต้องกลัวน้า กอดๆ {message.author.mention}")
    elif content == "ไม่กอด":
        await message.channel.send(f"เสียจัยน่ะ {message.author.mention}")
    elif content in ["ใจ","จัย"]:
        await message.channel.send(f"ไม่สนใจแล้ว {message.author.mention}")
    elif content in ["ฝันดี","นอน","หลับ"]:
        await message.channel.send(f"ฝันดีน่ะ จุ๊บ {message.author.mention}")
    elif content == "ไม่":
        await message.channel.send(f"แง่ๆ {message.author.mention}")
    elif content == "เบื่อ":
        await message.channel.send(f"ไม่ให้เบื่อ {message.author.mention}")
    elif content == "สัส":
        await message.channel.send(
            f"อะไรน่ะสุดหล่อ สัสเลยหรอ {message.author.mention}"
        )
        await message.delete()

    elif content in ["ใช่", "ช่าย"]:
        await message.channel.send(f"โอเค {message.author.mention}")

    elif content == "ค":
        await message.channel.send(
            f"ย่อได้ดีแต่ฉันรู้นะว่าจะพิมพ์อะไร {message.author.mention}"
        )
    
        await message.delete()
    else:
        await message.channel.send(f"ไม่เข้าใจแฮะ {message.author.mention}")
    await bot.process_commands(message)

# เปิด server (กันบอทหลับ)
server_on()

# รันบอท
bot.run(TOKEN)


