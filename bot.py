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

# ===== MEMORY CHAT =====
# หมายเหตุ: ข้อมูลจะหายถ้าบอท Restart
custom_responses = {}

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

    # ถ้าเป็นคำสั่ง Prefix ให้ทำงานตามคำสั่งแล้วหยุด
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # ===== BAD WORD CHECK =====
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except discord.Forbidden:
                print("ไม่มีสิทธิ์ลบข้อความ")
            except Exception as e:
                print(f"Error: {e}")
            
            await message.channel.send(
                f"{message.author.mention} ใช้คำสุภาพหน่อยน้า",
                delete_after=5
            )
            return # หยุดการทำงานทันทีเมื่อเจอคำหยาบ

    # ===== TEACH BOT (ต้องตอบ...) =====
    if "ต้องตอบ" in raw: # ใช้ raw เพื่อให้แยกคำว่าง่ายขึ้น
        try:
            # ใช้ raw เพื่อรักษาความหมายต้นฉบับก่อนแยก =
            data = raw.replace("ต้องตอบ", "").strip()
            if "=" in data:
                key, value = data.split("=", 1)
                key_clean = clean_text(key)
                custom_responses[key_clean] = value.strip()

                await message.reply(
                    f"จำแล้วน้า 👍\nถ้ามีคนพิมพ์ว่า **{key.strip()}** เราจะตอบว่า\n> {value.strip()}"
                )
                return
        except:
            await message.reply(
                f"รูปแบบไม่ถูกน้า 😅\nใช้แบบนี้:\n`ต้องตอบ คำถาม=คำตอบ`"
            )
            return

    # ===== CUSTOM RESPONSE (จากที่สอนไว้) =====
    if content in custom_responses:
        await message.reply(custom_responses[content]) 
        return

    # ===== RANDOM LETTER CHECK (ก-ฮ ตัวเดียว) =====
    if re.fullmatch(r"[ก-ฮa-zA-Z]", raw):
        await message.reply(f"จะรอพิมพ์น่ะ")
        return

    # ===== KEYWORDS CHAT =====
    if content.startswith("สวัสดี"):
        await message.reply("สวัสดีเป็นไงบ้างวันนี้~ มาแบบสบาย ๆ หรือมีอะไรอยากคุยไหม")
        return

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.reply("ดีจ้า")
        return

    elif content in ["hi", "hello"]:
        await message.reply("hello")
        return

    elif "คิดถึง" in content:
        await message.reply("คิดถึงเหมือนกันนะ 🌱")
        return

    elif "cry" in content:
        await message.reply("เฮ้… ถ้ามันหนักก็ร้องออกมาได้นะ 🫂")
        return

    elif any(x in content for x in ["ทำอะไรได้", "ทำไรได้"]):
        await message.reply("คุย เล่นมุก เขียนโค้ดให้ได้")
        return

    elif "ไม่รู้" in content:
        await message.reply("โอเครๆ ถ้ายังไม่รู้เดี๋ยวก็รู้เองน่ะ")
        return

    elif "เบื่อ" in content:
        await message.reply("เบื่ออออ 😩 เข้าใจเลยนะงั้นเอาแบบสั้น ๆ ก่อนเลือกมาอย่างนึง👇1️⃣ คุยเล่นมั่ว ๆ ขำ ๆ2️⃣ ให้เราโยนเกม/คำถามแปลก ๆ ใส่3️⃣ เล่าอะไรให้ฟังสักเรื่อง (ลึกลับ ขำ ดราม่า เลือกได้)4️⃣ ระบายมาเลย เราฟังอยู่5️⃣ เขียนโค้ดเล่น ๆ แก้เบื่อก็ได้ 😏หรือถ้าไม่อยากเลือก…เราขอถามนิดเดียว: เบื่อแบบ ง่วง / เหงา / เซ็ง / หมดไฟ แบบไหน?")
        return

    elif content in ["ไง", "ว่าไง", "งาย", "ว่างาย"]:
        await message.reply("ว่าไง~ เป็นยังไงบ้างวันนี้")
        return

    elif any(x in content for x in ["ฝันดี", "นอน"]):
        await message.reply("ฝันดีน้า หลับสบาย 😊")
        return

    elif any(x in content for x in ["ใครคือsun", "sunคือใคร"]):
        await message.reply("เราไง ๆ")
        return

    elif "?" in raw:
        await message.reply("สงสัยอะไรหรอ")
        return

    # ===== CODE SNIPPETS =====
    elif any(x in content for x in ["php", "css", "html", "โค้ด"]):
        sent_code = False
        if "php" in content or "โค้ด" in content:
            await message.reply("```php\n<?php\n$name=trim($_POST[\"name\"]);\n$age=trim($_POST[\"age\"]);\n$sex=trim($_POST[\"sex\"]);\n$file=\"name.xls\";\n$ff= !file_exists($file) || filesize($file)==0;\n$f=fopen($file,\"a\");\nif($name==\"sun\"){\n    header(\"Location: admin.html\");\n    return 0;\n}\nif($ff){\n    fwrite($f, \"name\\tage\\n\");\n}\nelseif($age>=100){\n    header(\"Location: 100++.html\");\n    return 0;\n}\nelseif($sex==\"line\"){\n    header(\"Location: [https://line.me/ti/p/biEKhMEh2y](https://line.me/ti/p/biEKhMEh2y)\");\n}\nelseif($sex==\"facebook\"){\n    header(\"Location: [https://www.facebook.com/kikixd88](https://www.facebook.com/kikixd88)\");\n}\nfwrite($f, $name.\"\\t\".$age.\"\\n\");\nfclose($f);\n?>\n```")
            sent_code = True
        
        if "css" in content or "โค้ด" in content:
            await message.reply("```css\n* { margin: 0; padding: 0; box-sizing: border-box; }\nbody { font-family: 'Prompt', sans-serif; background: #94ffb4; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }\n.login-container { background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); border: 1px solid #e0e0e0; padding: 40px; width: 100%; max-width: 420px; animation: fadeIn 0.5s ease-in; }\n```")
            sent_code = True

        if "html" in content or "โค้ด" in content:
            await message.reply("```html\n<!DOCTYPE html>\n<html lang=\"th\">\n<head>\n    <meta charset=\"UTF-8\">\n    <title>Form</title>\n    <link rel=\"stylesheet\" href=\"color.css\">\n</head>\n<body>\n    <form method=\"post\" action=\"data.php\">\n        <label for=\"name\">ชื่อ</label>\n        <input type=\"text\" id=\"name\" name=\"name\" required minlength=\"2\">\n        <label for=\"age\">อายุ</label>\n        <input type=\"number\" id=\"age\" name=\"age\" required min=\"5\">\n        <div>\n            <input type=\"radio\" id=\"facebook\" name=\"sex\" value=\"facebook\" required>\n            <label for=\"facebook\">เฟส</label>\n            <input type=\"radio\" id=\"line\" name=\"sex\" value=\"line\">\n            <label for=\"line\">ไลน์</label>\n        </div>\n        <button type=\"submit\">ส่ง</button>\n    </form>\n</body>\n</html>\n```")
            sent_code = True
        
        if sent_code:
            return

    # ===== FALLBACK (ถ้าไม่เข้าเงื่อนไขไหนเลย) =====
    else:
        fallback = ["อืม ", "เล่าต่อสิ", "เข้าใจๆ", "โอเคเลย", "ฟังอยู่นะ"]
        await message.reply(random.choice(fallback))

# ===== RUN =====
server_on()
bot.run(TOKEN)
