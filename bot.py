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
    # 2️⃣ ตัวอักษรมั่ว
    # =====================
    if re.fullmatch(r"[ก-ฮ]", raw):
        await message.channel.send(f"รอพิมพ์ให้ครบน่ะ {message.author.mention}")
        return

    elif re.fullmatch(r"[ก-ฮ]+", raw) or re.fullmatch(r"[a-zA-Z]+", raw):
        await message.channel.send(f"พิมพ์ไม่ครบหรอ {message.author.mention}")
        return

    # =====================
    # 3️⃣ KEYWORDS
    # =====================
    if content.startswith("สวัสดี"):
        await message.channel.send(f"สวัสดี {message.author.mention}")
    elif content.startswith("ค"):
        await message.delete()
    elif "@" in content:
        return

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้า {message.author.mention}")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention}")

    elif "ไม่รู้" in content:
        await message.channel.send(f"ทำไมไม่รู้ {message.author.mention}")
    elif "ประชด" in content:
        await message.channel.send(f"ขอโทษแล้วกันที่ทำไม่ได้ทุกอย่างTT {message.author.mention}")
    elif "เบลอ" in content:
        await message.channel.send(f"ไม่เบลอแล้ว {message.author.mention}")
    elif "ไง" in content:
        await message.channel.send(f"ว่าไง {message.author.mention}")
    elif "คิดถึง" in content:
        await message.channel.send(f"คิดถึง {message.author.mention}")
    elif "นายคิดยังไงกับเราหรอ" in content:
        await message.channel.send(f"ก็ไม่รู้สิเราไม่ได้จำว่านายเป็นยังไงแต่ก็คิดว่านายน่าจะเป็นคนดี {message.author.mention}")
    elif "หัวเราะทำไม" in content:
        await message.channel.send(f"ขอโทษทีๆ {message.author.mention}")

    elif "ใครคือsun" in content or "sunคือใคร" in content:
        await message.channel.send(f"เราไง {message.author.mention}")

    elif "ไม่ชอบ" in content:
        await message.channel.send(f"เราก็ไม่ชอบ {message.author.mention}")
    elif "เขียนเองดีกว่าเยอะเนอะ" in content:
        await message.channel.send(f"ใช่ๆ {message.author.mention}")

    elif "ทำอะไรได้" in content or "ทำไรได้" in content:
        await message.channel.send(f"ทำได้หลายอย่างเลย {message.author.mention}")

    elif "กลัว" in content:
        await message.channel.send(f"ไม่ต้องกลัวนะ {message.author.mention}")

    elif "ฝันดี" in content or "นอน" in content or "นอนล่ะ" in content:
        await message.channel.send(f"ฝันดีนะ {message.author.mention}")

    elif "ทำไร" in content:
        await message.channel.send(f"ก็คุยกับคุณไง {message.author.mention}")

    elif "คิดว่าไง" in content:
        await message.channel.send(f"ก็ดีนะ {message.author.mention}")

    elif "จริงหรอ" in content or "จริงไหม" in content:
        await message.channel.send(f"จริงแน่นอน {message.author.mention}")

    elif content == "ไม่":
        await message.channel.send(f"แย่จัง {message.author.mention}")

    elif "1+1" in content:
        await message.channel.send(f"Hello world ไง {message.author.mention}")

    elif "เค" in content:
        await message.channel.send(f"โอเคร {message.author.mention}")

    elif "?" in raw:
        await message.channel.send(f"งงอะไรหรอ {message.author.mention}")
    elif "เป็นไง" in raw:
        await message.channel.send(f"สบายดี {message.author.mention}")
    elif "เล่าอะไร" in raw:
        await message.channel.send(f" งั้นไม่ต้องเล่ากะด้ายเพราะเราก็ไม่รู้ว่าจะให้เล่าอะไรเหมือนกาน{message.author.mention}")
    elif "เข้าใจ" in content or "เข้าจัย" in content:
        await message.channel.send(f"โอเครเข้าใจสิน่ะ {message.author.mention}")
    elif "อรุณสวัสดิ์" in content or "morning" in content:
        await message.channel.send(f"อรุณสวัสดิ์ {message.author.mention}")
    

    # =====================
    # 4️⃣ PHP RESPONSE
    # =====================
    elif "php" in content:
        php_code = """```php
<?php
$name = trim($_POST["name"]);
$age  = trim($_POST["age"]);

$file = "name.xls";
$first = !file_exists($file) || filesize($file) == 0;
$f = fopen($file, "a");

if ($first) {
    fwrite($f, "Name\\tAge\\n");
}

if ($name == "sun" && $age == 18) {
    header("Location: oksun.html");
    exit;
} elseif ($age <= 100) {
    header("Location: https://www.youtube.com/watch?v=T_73H-pbAgw");
    exit;
}

fwrite($f, $name . "\\t" . $age . "\\n");
fclose($f);
?>
```"""
        await message.channel.send(php_code)
        await message.channel.send(message.author.mention)
    elif "html" in content:
        html_code = """```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form method="post" action="data.php">
        <label for="name">name</label>
        <br>
        <input type="text" name="name">
        <br>
        <label for="age">age</label>
        <br>
        <input type="number" name="age">
        <br>
        <button type="submit">x</button>
    </form>
</body>

</html>
```"""
        await message.channel.send(html_code)
        await message.channel.send(message.author.mention)

    elif "ดี" in content:
        await message.channel.send(f"ขอบคุณ {message.author.mention}")

    elif "หรอ" in content:
        await message.channel.send(f"ใช่ {message.author.mention}")

    # =====================
    # 5️⃣ FALLBACK
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








