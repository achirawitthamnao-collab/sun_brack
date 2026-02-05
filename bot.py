import discord
from discord.ext import commands
import os
import re
import random
import sqlite3
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("❌ ไม่พบ DISCORD_TOKEN ใน Environment Variables")

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DATABASE SETUP =====
db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS booster (
    user_id INTEGER PRIMARY KEY
)
""")
db.commit()

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Bot ready as {bot.user}")

@bot.event
async def on_member_update(before, after):
    role_boost = after.guild.premium_subscriber_role

    # เริ่มบูสต์
    if role_boost not in before.roles and role_boost in after.roles:
        cursor.execute(
            "INSERT OR IGNORE INTO booster (user_id) VALUES (?)",
            (after.id,)
        )
        db.commit()
        channel = after.guild.system_channel
        if channel:
            await channel.send(
                f"💜 ขอบคุณ {after.mention} ที่บูสต์เซิร์ฟเวอร์!"
            )

    # เลิกบูสต์
    if role_boost in before.roles and role_boost not in after.roles:
        cursor.execute(
            "DELETE FROM booster WHERE user_id = ?",
            (after.id,)
        )
        db.commit()

# ===== COMMANDS =====
@bot.command()
async def boosters(ctx):
    cursor.execute("SELECT user_id FROM booster")
    rows = cursor.fetchall()

    if not rows:
        await ctx.send("ยังไม่มีคนบูสต์เลย 😭")
        return

    mentions = []
    for (uid,) in rows:
        member = ctx.guild.get_member(uid)
        if member:
            mentions.append(member.mention)

    await ctx.send("💎 ผู้สนับสนุนเซิร์ฟเวอร์:\n" + "\n".join(mentions))

# ===== RUN =====
bot.run(TOKEN)
