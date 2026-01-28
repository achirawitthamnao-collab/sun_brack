# ไฟล์: myserver.py
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running! | สถานะ: ปกติ"

def run():
    # Render ต้องการให้รันบน 0.0.0.0
    app.run(host='0.0.0.0', port=8080)

def server_on():
    t = Thread(target=run)
    t.start()
