from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=10000)

def server_on():
    Thread(target=run).start()
