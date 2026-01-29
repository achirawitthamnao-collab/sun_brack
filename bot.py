import discord
from discord.ext import commands
import os
import re
import random
import json
from dotenv import load_dotenv
from myserver import server_on

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== ระบบจัดการไฟล์ความจำ =====
def load_responses():
    try:
        if os.path.exists("responses.json"):
            with open("responses.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        return {}
    return {}

def save_responses(data):
    with open("responses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^ก-๙a-z0-9]", "", text)
    return text

bad_words = ["ควย", "เหี้ย", "สันดาน", "หี", "หรรม", "หำ", "โง่", "กาก", "กระจอก"]

@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ออนไลน์แล้ว (ระบบความจำ JSON)")

# ===== คำสั่งสอนบอทแบบเงียบๆ =====
@bot.command()
async def จำ(ctx, *, text: str):
    if "|" in text:
        parts = text.split("|")
        key = clean_text(parts[0].strip())
        value = parts[1].strip()
        
        data = load_responses()
        data[key] = value
        save_responses(data)
        # ตอบรับสั้นๆ ว่าจำแล้ว
        await ctx.message.add_reaction("✅") 

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw = message.content.strip()
    content = clean_text(raw)

    # 1. เช็คคำหยาบ
    for word in bad_words:
        if word in content:
            try: await message.delete()
            except: pass
            await message.channel.send(f"{message.author.mention} ใช้คำสุภาพหน่อยน้า", delete_after=5)
            return

    # 2. เช็คตัวอักษรเดียว
    if re.fullmatch(r"[ก-ฮa-zA-Z]", raw):
        await message.channel.send(f"จะรอพิมพ์น่ะ {message.author.mention}")
        return

    # 3. เช็คจากความจำใน JSON (รวมคำถามทั้งหมดไว้ที่นี่)
    custom_data = load_responses()
    
    # วนลูปเช็คคำถามในไฟล์ (เพื่อให้รองรับการเช็คแบบ "มีคำนั้นอยู่ในประโยค")
    for key, response in custom_data.items():
        if key in content:
            await message.channel.send(f"{response} {message.author.mention}")
            return

    # 4. เงื่อนไขพิเศษที่ต้องใช้โค้ด (เช่น PHP/HTML หรือการตอบแบบสุ่ม)
    if "php" in content:
        await message.channel.send("```php\n<?php\n// โค้ด PHP ของคุณ\n?>\n```")
        return

    elif "html" in content or "โค้ด" in content:
        await message.channel.send("```html\n<!DOCTYPE html>\n<html>...</html>\n```")
        return

    elif "?" in raw:
        await message.channel.send(f"สงสัยอะไรหรอ {message.author.mention}")
        return

    # 5. FALLBACK (ถ้าไม่เจอคำถามที่ตรงเลย)
    else:
        fallback = ["อืม 🤔", "เล่าต่อสิ", "เข้าใจๆ", "ฟังอยู่นะ", "ออเครๆ"]
        await message.channel.send(f"{random.choice(fallback)} {message.author.mention}")

    await bot.process_commands(message)

server_on()
bot.run(TOKEN)
