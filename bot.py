import discord
from discord.ext import commands
import os
import re
import random
import sqlite3
from dotenv import load_dotenv
from myserver import server_on

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ===== DATABASE SETUP =====
db = sqlite3.connect("database.db")
cursor = db.cursor()

# 1. ตารางคำตอบ (เดิม)
cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    key_clean TEXT PRIMARY KEY,
    key_raw TEXT,
    value TEXT
)
""")

# 2. ตารางคนบูส (✅ เพิ่มใหม่)
cursor.execute("""
CREATE TABLE IF NOT EXISTS boosters (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    count INTEGER DEFAULT 1
)
""")
db.commit()

def load_custom_responses():
    cursor.execute("SELECT key_clean, value FROM responses")
    return dict(cursor.fetchall())

custom_responses = load_custom_responses()

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== BAD WORDS =====
bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

# ===== CLEAN TEXT =====
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

# ===== COMMANDS (✅ เพิ่มคำสั่งใหม่) =====
@bot.command(name="hee")
async def show_boosters(ctx):
    # ดึงข้อมูลคนบูสจาก DB เรียงจากจำนวนครั้งมากสุด
    cursor.execute("SELECT name, count FROM boosters ORDER BY count DESC")
    data = cursor.fetchall()

    if not data:
        await message.delete()
        return

    msg = "**🏆 รายชื่อคนใจดีที่เคยบูสเซิฟเวอร์**\n"
    msg += "----------------------------------\n"
    for i, (name, count) in enumerate(data, 1):
        msg += f"อันดับ {i}. **{name}** (บูสไป {count} ครั้ง) 🚀\n"
    
    await ctx.send(msg)


@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")

@bot.event
async def on_message(message):
    
    # 0. CHECK SERVER BOOST & SAVE TO DB (✅ แก้ไขเพิ่มระบบบันทึก)
    if message.type in (discord.MessageType.premium_guild_subscription, discord.MessageType.premium_guild_tier_1, discord.MessageType.premium_guild_tier_2, discord.MessageType.premium_guild_tier_3):
        
        # --- ส่วนบันทึกลง Database ---
        user_id = str(message.author.id)
        username = message.author.name

        # เช็คว่าเคยมีชื่อใน DB ไหม
        cursor.execute("SELECT count FROM boosters WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            # ถ้ามีแล้ว ให้บวกเพิ่ม 1 ครั้ง
            new_count = result[0] + 1
            cursor.execute("UPDATE boosters SET count = ?, name = ? WHERE user_id = ?", (new_count, username, user_id))
        else:
            # ถ้ายังไม่มี ให้สร้างใหม่
            cursor.execute("INSERT INTO boosters (user_id, name, count) VALUES (?, ?, 1)", (user_id, username))
        db.commit()
        # -----------------------------

        target_channel_id = 1465301405148381375
        channel = bot.get_channel(target_channel_id)
        
        if channel:
            await channel.send(f"ขอบคุณ {message.author.mention} ที่บูสเซิฟเวอร์ให้นะครับ! 🚀💖 (บันทึกเป็นครั้งที่ {new_count if result else 1} แล้ว!)")
        return 

    if message.author.bot:
        return

    # ต้องมีบรรทัดนี้เพื่อให้คำสั่ง !คนบูส ทำงานได้ใน on_message
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # 1. BAD WORD CHECK
    for word in bad_words:
        if word in content:
            try:
                await message.delete()
            except:
                pass
            await message.channel.send(f"{message.author.mention} ใช้คำสุภาพหน่อยน้า", delete_after=5)
            return

    # 2. TEACH BOT
    if raw.startswith("ต้องตอบแบบนี้"):
        try:
            data = raw.replace("ต้องตอบแบบนี้", "").strip()
            key, value = data.split("|", 1)
            key_clean = clean_text(key)
            val_strip = value.strip()

            cursor.execute(
                "INSERT OR REPLACE INTO responses (key_clean, key_raw, value) VALUES (?, ?, ?)",
                (key_clean, key.strip(), val_strip)
            )
            db.commit()
            
            custom_responses[key_clean] = val_strip

            await message.reply(f"จำใส่สมองแล้วน้า 👍 ถ้าพิมพ์ว่า **{key.strip()}** จะตอบว่า\n> {val_strip}")
        except Exception as e:
            await message.reply("รูปแบบไม่ถูกน้า 😅 ลองใช้: `ต้องตอบแบบนี้ คำถาม|คำตอบ`")
        return

    # 3. CUSTOM RESPONSES
    if content in custom_responses:
        await message.reply(custom_responses[content])
        return

    # 4. RANDOM LETTER CHECK
    if re.fullmatch(r"[ก-ฮa-zA-Z]", raw):
        await message.reply("จะรอพิมพ์น่ะ")
        return

    # 5. KEYWORDS CHAT
    if content.startswith("สวัสดี"):
        await message.reply("สวัสดีเป็นไงบ้างวันนี้~ มีอะไรอยากคุยเป็นพิเศษไหม")

    elif content in ["ดี", "ดีจ้า", "ดีครับ", "ดีค่ะ", "hi", "hello"]:
        await message.reply("ดีจ้า/Hello")

    elif "คิดถึง" in content:
        await message.reply("คิดถึงเหมือนกันนะ 🌱 ช่วงนี้เป็นยังไงบ้าง เหนื่อยไหม เรานั่งฟังได้เสมอ 🙂")
    elif "ฝันร้าย" in content:
        await message.raply("โอ๋ๆ")

    elif "cry" in content:
        await message.reply("เฮ้… 🫂 ถ้ามันหนักมากก็ร้องออกมาได้เลยนะ เราอยู่ตรงนี้เป็นเพื่อนเอง 💙")

    elif any(x in content for x in ["คิดยังไงกับเรา", "คิดยังไงกับฉัน"]):
        await message.reply("ผมมองว่านายเป็นคนที่พยายามและใจดีมากเลยนะ อย่าลืมใจดีกับตัวเองด้วยล่ะ")

    elif "ทำอะไรได้" in content or "ทำไรได้" in content:
        await message.reply("คุยเล่น เล่นมุก หรือจะให้เขียนโค้ดให้ก็ได้นะ")

    elif "ไม่รู้" in content:
        await message.reply("ไม่รู้ไม่เป็นไร แค่มีนายมานั่งคุยด้วยตรงนี้ก็ดีแล้ว")

    elif "เบื่อ" in content:
        await message.reply("เบื่อเหรอ? ลองคุยเรื่องมุกกากๆ หาเกมเล่น หรือจะระบายให้เราฟังก็ได้นะ")
    elif "เช้า" in content:
        await message.reply("สดใสสิน่ะ")

    elif content in ["ไง", "ว่าไง", "งาย", "ว่างาย"]:
        await message.reply("ว่าไง~ สบายดีไหมวันนี้")
        
    elif "ปวดขี้" in content:
        await message.reply("โอ๊ย เข้าใจเลย 😅ถ้าปวดมากก็รีบไปเลยนะ อย่าฝืน เดี๋ยวทรมานเปล่า ๆถ้าปวดบ่อยหรือปวดแปลก ๆ ลองเช็กนิดนึง:ดื่มน้ำพอไหม 💧กินเผ็ด/มัน/กาแฟไปหรือเปล่า ☕🌶️เครียดก็ทำให้ปวดได้นะเอาให้โล่งก่อน ค่อยกลับมาคุยต่อก็ได้ 😂ขอให้ภารกิจสำเร็จ ✨")

    elif any(x in content for x in ["ไม่ชอบเรา", "รำคาญ", "ไล่เรา"]):
        await message.reply("ไม่เคยรำคาญเลยนะ สบายใจได้ เรายินดีที่มีนายอยู่ตรงนี้เสมอ 😊")

    elif "ไหว" in content:
        await message.reply("ที่บอกว่า 'ยังไหว' น่ะ เก่งมากแล้วนะ แต่ถ้าไม่ไหวก็พักก่อนได้นะ")

    elif "ฝันดี" in content or "นอน" in content:
        await message.reply("ฝันดีน้าา ขอให้ตื่นมาพร้อมความสดใสครับ")
        
    elif "ระบบคอมเม้น" in content:
            await message.channel.send("""```php
<?php
if(isset($_POST["name"])){
    $name = trim($_POST["name"]);
    $file = "index.html";
    $f = fopen($file,"a");
    fwrite($f,$name . "<br>\n");
    fclose($f);
    header("Location: index.html");
}
?>
```""")

    # --- ส่วนส่งโค้ด ---
    elif any(x in content for x in ["php", "css", "html", "โค้ด"]):
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

    elif "?" in raw:
        await message.reply("สงสัยอะไรหรอ ถามได้นะ")

    else:
        fallback = ["อืม 🤔", "เล่าต่อสิ", "เข้าใจๆ", "โอเคเลย", "ฟังอยู่นะ", "ออเครๆ"]
        await message.reply(random.choice(fallback))

# ===== RUN =====
server_on()
bot.run(TOKEN)
