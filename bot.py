import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

# ถ้าไม่ได้รันบน Replit หรือ Server ที่ต้องเปิด port ให้ลบบรรทัดนี้กับ server_on() ด้านล่างออกได้ครับ
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
    # ลบ space ทิ้งทั้งหมด (ระวัง: ถ้าพิมพ์ "sun ดีมาก" จะกลายเป็น "sunดีมาก")
    text = re.sub(r"\s+", "", text)             
    # เก็บภาษาไทย, อังกฤษ, ตัวเลข ไว้
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)    
    return text


@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")


@bot.event
async def on_message(message):
    # ป้องกันบอทคุยกับตัวเอง
    if message.author == bot.user:
        return

    raw = message.content
    content = clean_text(raw)

    # 1. เช็คคำหยาบก่อน (Bad Words)
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except discord.Forbidden:
                print("ไม่มีสิทธิ์ลบข้อความ (Missing Permissions)")
            except:
                pass
            
            await message.channel.send(
                f"{message.author.mention} กรุณาใช้คำสุภาพนะ"
            , delete_after=5) # ลบคำเตือนทิ้งหลัง 5 วิ เพื่อไม่ให้รก
            return # จบการทำงานทันทีถ้าเจอคำหยาบ

    # 2. เช็ค Keyword การตอบโต้
    # ใช้ if ทั้งหมด หรือ elif ก็ได้ แต่ต้องระวังลำดับ
    
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

    elif content in ["เปล่า", "ป่าว"]:
        await message.channel.send(f"ดีแล้วที่ไม่เป็นไร {message.author.mention}")

    elif "sun" in content:
        await message.channel.send(
            f"เราเองๆ เป็นแสงสว่างท่ามกลางความมืด! {message.author.mention}"
        )

    elif content in ["ส", "สว", "สวั", "สวัส", "สวัสด"]:
        await message.channel.send(f"สวัสดีใช่ไหม {message.author.mention}")
        
    elif "ฮ" in content or "หะ" in content:
        await message.channel.send(f"ฮะอะไรน่ะ {message.author.mention}")
        
    elif "ทำไร" in content:
        await message.channel.send(f"นอน {message.author.mention}")
        
    elif "ได้ด้วยหรอ" in content:
        await message.channel.send(f"ได้แน่นอนสิ {message.author.mention}")
        
    elif "ทำ" in content: # ระวังคำนี้กว้างมาก เช่น "กำลังทำกับข้าว" บอทจะตอบว่า "จัดมาเลย"
        await message.channel.send(f"จัดมาเลย {message.author.mention}")
        
    elif "cry" in content:
        await message.channel.send(f"จะร้องทัมมายเนี่ยโอ๋ๆ {message.author.mention}")
        
    elif "emoji_62" in content:
        await message.channel.send(f"มีไรหรอเปล่า {message.author.mention}")
        
    elif "look" in content:
        await message.channel.send(f"ส่องอารายล่ะ {message.author.mention}")
        
    elif "eat" in content:
        await message.channel.send(f"กินด้วย {message.author.mention}")
        
    elif "baer" in content: # แก้ Baer เป็น baer (ตัวเล็ก)
        await message.channel.send(f"ห้ะ {message.author.mention}")
        
    # --- ลบส่วน else ที่ตอบว่า "ไม่เข้าใจแฮะ" ออก เพื่อไม่ให้ spam ---

    # 3. ประมวลผลคำสั่ง (เช่น !help, !play)
    await bot.process_commands(message)

# รัน Server
server_on()
bot.run(TOKEN)
