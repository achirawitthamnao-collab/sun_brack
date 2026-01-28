from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Bot is working! (Status: OK)"

def run():
    # ใช้ port 10000 ตามที่คุณตั้งไว้
    app.run(host="0.0.0.0", port=10000)

def server_on():
    t = Thread(target=run)
    t.start()
