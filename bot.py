import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from myserver import server_on  # ต้องมีไฟล์นี้จริง

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bad_words = ["ควย","เหี้ย","สันดาน","หี","หรรม","หำ","โง่","กาก","กระจอก"]

@bot.event
async def on_ready():
    print("ok")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    for word in bad_words:
        if word in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} กรุณาใช้คำสุภาพนะ (ตรวจพบคำว่า: {word})"
            )
            return

    if content == "สวัสดี":
        await message.channel.send(f"สวัสดี {message.author.mention}")

    elif content == "อะไรล่ะนั่น":
        await message.channel.send(f"ไม่รู้เหมือนกัน {message.author.mention}")

    elif len(content) > 59:
        await message.channel.send(f"ยาวจัง {message.author.mention}")

    elif content == "สัส":
        await message.channel.send(f"อะไรน่ะสุดหล่อ สัสเลยหรอ {message.author.mention}")
        await message.delete()

    elif content in ["ส", "สว", "สวั", "สวัส", "สวัสด"]:
        await message.channel.send(f"สวัสดีใช่ไหม {message.author.mention}")

    elif content in ["ใช่", "ช่าย"]:
        await message.channel.send(f"โอเค {message.author.mention}")

    elif content == "ค":
        await message.channel.send(
            f"ย่อได้ดีแต่ฉันรู้นะว่าจะพิมพ์อะไร {message.author.mention}"
        )
        await message.delete()

    await bot.process_commands(message)

server_on()        # ✅ แก้ชื่อถูกแล้ว
bot.run(TOKEN)
