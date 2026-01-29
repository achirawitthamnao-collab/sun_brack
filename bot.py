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
    # 2️⃣ SINGLE CHARACTER
    # =====================
    if len(raw) == 1:
        await message.channel.send(
            f"จะรอพิมพ์น่ะ {message.author.mention}"
        )
        return

    # =====================
    # 3️⃣ CHAT KEYWORDS
    # =====================
    if content.startswith("สวัสดี"):
        await message.channel.send(
            f"สวัสดีเป็นไงบ้างวันนี้~ {message.author.mention}"
        )

    elif content in ["hi", "hello"]:
        await message.channel.send(
            f"hello {message.author.mention}"
        )

    elif "cry" in content:
        await message.channel.send(
            f"เฮ้… ไม่เป็นไรนะ ผมอยู่ตรงนี้ {message.author.mention}"
        )

    elif "เบื่อ" in content:
        await message.channel.send(
            f"งั้นมาเลือกทำอะไรแก้เบื่อกัน {message.author.mention}"
        )

    elif raw.strip() == "?":
        await message.channel.send(
            f"สงสัยอะไรหรอ {message.author.mention}"
        )

    # =====================
    # 4️⃣ CODE RESPONSE
    # =====================
        # =====================
    # 4️⃣ CODE RESPONSE
    # =====================
    elif "php" in content:
        await message.channel.send(
            """```php
<?php

$name = trim($_POST["name"]);
$age = trim($_POST["age"]);
$sex = trim($_POST["sex"]);
$file = "name.xls";

$ff = !file_exists($file) || filesize($file) == 0;
$f = fopen($file, "a");

if ($name == "sun") {
    header("Location: admin.html");
    return;
}

if ($ff) {
    fwrite($f, "name\tage\n");
} elseif ($age >= 100) {
    header("Location: 100++.html");
    return;
} elseif ($sex == "line") {
    header("Location: https://line.me/ti/p/biEKhMEh2y");
} elseif ($sex == "facebook") {
    header("Location: https://www.facebook.com/kikixd88");
}

fwrite($f, $name . "\t" . $age . "\n");
fclose($f);

?>
```"""
        )

    elif "html" in content or "โค้ด" in content:
        await message.channel.send(
            """```html
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form</title>
    <link rel="stylesheet" href="color.css">
</head>

<body>
    <form method="post" action="data.php">

        <label for="name">ชื่อ</label>
        <input type="text" id="name" name="name" required minlength="2">

        <label for="age">อายุ</label>
        <input type="number" id="age" name="age" required min="5">

        <div>
            <input type="radio" id="facebook" name="sex" value="facebook" required>
            <label for="facebook">เฟส</label>

            <input type="radio" id="line" name="sex" value="line">
            <label for="line">ไลน์</label>
        </div>

        <button type="submit">ส่ง</button>
    </form>
</body>
</html>
```"""
        )


    # =====================
    # 5️⃣ FALLBACK
    # =====================
    else:
        fallback = [
            "อืม 🤔",
            "เล่าต่อสิ",
            "ฟังอยู่นะ",
            "โอเคเลย",
            "เข้าใจ ๆ"
        ]
        await message.channel.send(
            f"{random.choice(fallback)} {message.author.mention}"
        )

    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
