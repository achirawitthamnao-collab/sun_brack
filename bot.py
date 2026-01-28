import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

# โหลดตัวแปร (สำหรับรันในคอม แต่บน Render ไม่ได้ใช้บรรทัดนี้ก็ไม่เป็นไร)
load_dotenv()

# ตั้งค่า Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ตั้งค่า Google Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# เช็คว่ามี Key ไหม (กันพลาด)
if not GEMINI_API_KEY:
    print("❌ ไม่พบ GEMINI_API_KEY ใน Environment!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# *** ใช้ชื่อรุ่นที่ถูกต้อง ***
model = genai.GenerativeModel('gemini-1.5-flash')

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # เช็คว่าบอททำงานไหม
    if message.content.startswith('สวัสดี'):
        await message.channel.send('สวัสดีครับ! พร้อมทำงานแล้ว 😎')
        return

    # คุยกับ AI
    try:
        async with message.channel.typing():
            # ส่งข้อความไปหา Gemini
            response = model.generate_content(message.content)
            
            # ตอบกลับ (ตัดข้อความถ้าเกิน 1900 ตัว)
            reply_text = response.text
            if len(reply_text) > 1900:
                reply_text = reply_text[:1900] + "...(ยาวไปตัดจบ)"
            
            await message.channel.send(reply_text)

    except Exception as e:
        # ฟ้อง Error ในแชททันที
        error_msg = f"❌ เกิดข้อผิดพลาด:\n```{str(e)}```"
        await message.channel.send(error_msg)
        print(error_msg)

# รันบอท
# ใช้ server_on() ถ้าจำเป็นต้องเปิด web server หลอก Render (ในไฟล์ myserver.py)
from myserver import server_on
server_on() 

client.run(os.getenv('DISCORD_TOKEN'))


