import discord
from discord.ext import commands
import os
import re
import random
import json
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
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

# ===== UTIL =====
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

# ===== MEMORY (JSON) =====
def load_responses():
    if not os.path.exists("responses.json"):
        with open("responses.json", "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    with open("responses.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(data):
    with open("responses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

responses_cache = load_responses()

# ===== READY =====
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ออนไลน์แล้ว (โหมดเพื่อนคุย)")

# ===== MAIN CHAT =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # 1️⃣ คำหยาบ
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(
                f"{message.author.mention} ใจเย็นน้า ใช้คำสุภาพหน่อย 🙂",
                delete_after=5
            )
            return

    # 2️⃣ ตัวอักษรเดียว
    if re.fullmatch(r"[ก-ฮa-z0-9]", content):
        await message.channel.send(f"พิมพ์มาอีกนิดสิ {message.author.mention}")
        return

    # 3️⃣ ตอบจากความจำ
    for key, value in responses_cache.items():
        if key in content and value:
            await message.channel.send(f"{value} {message.author.mention}")
            return

    # 4️⃣ PHP
    if "php" in content:
        await message.channel.send("""```php
<?php

$name=trim($_POST["name"]);
$age=trim($_POST["age"]);
$sex=trim($_POST["sex"]);
$file="name.xls";

$ff= !file_exists($file) || filesize($file)==0;

$f=fopen($file,"a");

if($name=="sun"){
    header("Location: admin.html");
    return 0;
}
if($ff){
    fwrite($f, "name\tage\n");
}
elseif($age>=100){
    header("Location: 100++.html");
    return 0;
}
elseif($sex=="line"){
    header("Location: https://line.me/ti/p/biEKhMEh2y");
}
elseif($sex=="facebook"){
    header("Location: https://www.facebook.com/kikixd88");
}


fwrite($f, $name."\t".$age."\n");
fclose($f);

?>
```""")
        return

    # 5️⃣ HTML
    if "html" in content or "โค้ด" in content:
        await message.channel.send("""```html
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
```""")
        return

    # 6️⃣ ถามมาใหม่ → เก็บเข้าความจำอัตโนมัติ
    if "?" in raw or len(content) >= 4:
        if content not in responses_cache:
            responses_cache[content] = ""
            save_responses(responses_cache)

        replies = [
            "อืม… น่าสนใจนะ 🤔",
            "เรายังไม่ค่อยรู้เหมือนกัน",
            "ฟังอยู่นะ เล่าต่อสิ",
            "ถามได้น่าคิดแฮะ"
        ]
        await message.channel.send(
            f"{random.choice(replies)} {message.author.mention}"
        )
        return

    # 7️⃣ fallback เพื่อน ๆ
    fallback = ["อ่ออ", "อืม", "ว่าไงต่อ", "ฟังอยู่นะ"]
    await message.channel.send(
        f"{random.choice(fallback)} {message.author.mention}"
    )

    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
