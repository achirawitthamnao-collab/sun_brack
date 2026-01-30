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
            except:
                pass
            await message.channel.send(
                f"{message.author.mention} ใช้คำสุภาพหน่อยน้า",
                delete_after=5
            )
            return

    # ===== RANDOM LETTER CHECK =====
    if re.fullmatch(r"[ก-ฮa-zA-Z]", raw):
        await message.channel.send(f"จะรอพิมพ์น่ะ {message.author.mention}")
        return

    # ===== TEACH BOT =====
    if raw.startswith("ต้องตอบแบบนี้"):
        try:
            data = raw.replace("ต้องตอบแบบนี้", "").strip()
            key, value = data.split("|", 1)

            key_clean = clean_text(key)
            custom_responses[key_clean] = value.strip()

            await message.channel.send(
                f"จำแล้วน้า 👍\nถ้ามีคนพิมพ์ว่า **{key}** เราจะตอบว่า\n> {value.strip()} {message.author.mention}"
            )
        except:
            await message.channel.send(
                f"รูปแบบไม่ถูกน้า 😅\nใช้แบบนี้:\n`ต้องตอบแบบนี้ คำถาม|คำตอบ` {message.author.mention}"
            )
        return

    # ===== CUSTOM RESPONSE =====
    if content in custom_responses:
        await message.channel.send(custom_responses[content])
        return

    # ===== KEYWORDS CHAT =====
    if content.startswith("สวัสดี"):
        await message.channel.send(
            f"สวัสดีเป็นไงบ้างวันนี้~ มาแบบสบาย ๆ หรือมีอะไรอยากคุยไหม {message.author.mention}"
        )

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ"]:
        await message.channel.send(f"ดีจ้า {message.author.mention}")

    elif content in ["hi", "hello"]:
        await message.channel.send(f"hello {message.author.mention}")

    elif "คิดถึง" in content:
        await message.channel.send(
            f"คิดถึงเหมือนกันนะ 🌱 {message.author.mention}"
        )

    elif "cry" in content:
        await message.channel.send(
            f"เฮ้… ถ้ามันหนักก็ร้องออกมาได้นะ 🫂 {message.author.mention}"
        )

    elif "ทำอะไรได้" in content or "ทำไรได้" in content:
        await message.channel.send(
            f"คุย เล่นมุก เขียนโค้ดให้ได้ {message.author.mention}"
        )

    elif "ไม่รู้" in content:
        await message.channel.send(
            f"ไม่เป็นไรเลย มานั่งเฉย ๆ ก็คุยได้ {message.author.mention}"
        )

    elif "เบื่อ" in content:
        await message.channel.send(
            f"เบื่อใช่ไหม เลือกเลย เดี๋ยวจัดให้ 😆 {message.author.mention}"
        )

    elif content in ["ไง", "ว่าไง", "งาย", "ว่างาย"]:
        await message.channel.send(
            f"ว่าไง~ เป็นยังไงบ้างวันนี้ {message.author.mention}"
        )

    elif "ฝันดี" in content or "นอน" in content:
        await message.channel.send(
            f"ฝันดีน้า หลับสบาย 😊 {message.author.mention}"
        )

    elif "ใครคือsun" in content or "sunคือใคร" in content:
        await message.channel.send(f"เราไง ๆ {message.author.mention}")

    elif "?" in raw:
        await message.channel.send(f"สงสัยอะไรหรอ {message.author.mention}")

    else:
        fallback = ["อืม 🤔", "เล่าต่อสิ", "เข้าใจๆ", "โอเคเลย", "ฟังอยู่นะ"]
        await message.channel.send(
            f"{random.choice(fallback)} {message.author.mention}"
        )
     elif "php" in content or "css" in content or "html" in content or "โค้ด" in content:
        if "php" in content or "โค้ด" in content:
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
    header("Location: [https://line.me/ti/p/biEKhMEh2y](https://line.me/ti/p/biEKhMEh2y)");
}
elseif($sex=="facebook"){
    header("Location: [https://www.facebook.com/kikixd88](https://www.facebook.com/kikixd88)");
}
fwrite($f, $name."\t".$age."\n");
fclose($f);
?>
```""")
        
        if "css" in content or "โค้ด" in content:
            await message.channel.send("""```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Prompt', sans-serif; background: #94ffb4; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
.login-container { background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); border: 1px solid #e0e0e0; padding: 40px; width: 100%; max-width: 420px; animation: fadeIn 0.5s ease-in; }
/* ... (โค้ด CSS ส่วนที่เหลือของคุณ) ... */
```""")

        if "html" in content or "โค้ด" in content:
            await message.channel.send("""```html
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
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

# ===== RUN =====
server_on()
bot.run(TOKEN)
