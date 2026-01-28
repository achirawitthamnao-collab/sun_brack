import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv
from myserver import server_on

# โหลดตัวแปรสภาพแวดล้อม
load_dotenv()

# ตั้งค่า Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ตั้งค่า Google Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# ตรวจสอบว่าใส่ Key หรือยัง
if not GEMINI_API_KEY:
    print("❌ Error: ไม่พบ GEMINI_API_KEY ใน Environment Variables")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# *** ใช้โมเดลรุ่น Flash (เร็วและฟรี) ***
# ถ้า requirements.txt อัปเดตแล้ว บรรทัดนี้จะทำงานได้ 100%
model = genai.GenerativeModel('gemini-1.5-flash')

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    print('Bot is ready to chat!')

@client.event
async def on_message(message):
    # ไม่ตอบข้อความของตัวเอง
    if message.author == client.user:
        return

    # เช็คสถานะบอทง่ายๆ
    if message.content.startswith('สวัสดี'):
        await message.channel.send('สวัสดีครับ! ผมพร้อมทำงานแล้วครับ 😎')
        return

    # ส่วนการคุยกับ AI
    try:
        # แสดงสถานะ "กำลังพิมพ์..."
        async with message.channel.typing():
            # ส่งข้อความไปหา Gemini
            response = model.generate_content(message.content)
            
            # ตรวจสอบความยาวข้อความ (Discord รับได้ไม่เกิน 2000 ตัว)
            reply_text = response.text
            if len(reply_text) > 1900:
                reply_text = reply_text[:1900] + "\n...(ข้อความยาวเกินไป ขอตัดจบแค่นี้นะครับ)"
            
            # ส่งคำตอบกลับไป
            await message.channel.send(reply_text)

    except Exception as e:
        # ถ้ามีปัญหา ให้แจ้งเตือนในแชททันที
        error_msg = f"❌ เกิดข้อผิดพลาดครับนายท่าน:\n```{str(e)}```"
        await message.channel.send(error_msg)
        print(error_msg)

# เปิด Server จำลองเพื่อให้ Render ไม่ปิดบอท
server_on()

# รันบอท
client.run(os.getenv('DISCORD_TOKEN'))
