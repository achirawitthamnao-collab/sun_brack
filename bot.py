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

# =====================
# 🧠 GIANT BRAIN 1000+
# =====================
brain = []

topics = {
    "ทำไร": ["ทำไร", "ทำอะไร", "ทำอยู่", "ว่างไหม", "ทำไรดี"],
    "ความรู้สึก": ["เหงา", "เบื่อ", "เครียด", "กลัว", "เหนื่อย", "คิดถึง"],
    "คำถาม": ["ทำไม", "จริงไหม", "ใช่ไหม", "หรอ", "?"],
    "ชีวิต": ["ชีวิต", "อนาคต", "ความฝัน", "โตขึ้น", "เป้าหมาย"]
}

answers_pool = {
    "ทำไร": [
        "ก็คุยกับคุณไง",
        "นั่งว่าง ๆ อยู่",
        "คิดอะไรไปเรื่อย"
    ],
    "ความรู้สึก": [
        "เข้าใจนะ",
        "ไม่เป็นไรหรอก",
        "เรายังอยู่นี่",
        "เดี๋ยวก็ดีขึ้น"
    ],
    "คำถาม": [
        "นั่นสิ",
        "ก็น่าคิดนะ",
        "อาจจะใช่ก็ได้",
        "ไม่แน่เหมือนกัน"
    ],
    "ชีวิต": [
        "ชีวิตมันซับซ้อนนะ",
        "ค่อย ๆ คิดก็ได้",
        "ไม่มีคำตอบเดียวหรอก"
    ]
}

# สร้างสมองพื้นฐาน
for topic, keys in topics.items():
    for k in keys:
        brain.append({
            "tags": [k],
            "answers": answers_pool[topic]
        })

# ยัดเพิ่มให้ครบ 1000+
while len(brain) < 1000:
    topic = random.choice(list(answers_pool.keys()))
    brain.append({
        "tags": [f"คำถามที่{len(brain)}"],
        "answers": answers_pool[topic]
    })

# =====================
# EVENTS
# =====================
@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user} | Brain size: {len(brain)}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # 1️⃣ BAD WORD CHECK
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

    # 2️⃣ ตัวอักษรมั่ว
    if re.fullmatch(r"[ก-ฮ]", raw):
        await message.channel.send(f"พิมพ์ตัวเดียวเองหรอ {message.author.mention}")
        return
    elif re.fullmatch(r"[ก-ฮ]+", raw) or re.fullmatch(r"[a-zA-Z]+", raw):
        await message.channel.send(f"พิมพ์แบบนี้ตอบไม่ได้แฮะ {message.author.mention}")
        return

    # 3️⃣ สมองยักษ์คิดคำตอบ
    matches = []

    for item in brain:
        score = 0
        for tag in item["tags"]:
            if tag in content or tag in raw:
                score += 1
        if score > 0:
            matches.append((score, item))

    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        best = matches[0][1]
        reply = random.choice(best["answers"])
        await message.channel.send(f"{reply} {message.author.mention}")
        return

    # 4️⃣ FALLBACK (บุคลิก)
    fallback = [
        "อืมม 🤔",
        "5555",
        "เล่าต่อสิ",
        "ฟังอยู่นะ",
        "น่าสนใจดี",
        "เข้าใจละ"
    ]
    await message.channel.send(
        f"{random.choice(fallback)} {message.author.mention}"
    )

    await bot.process_commands(message)

# ===== RUN =====
server_on()
bot.run(TOKEN)
