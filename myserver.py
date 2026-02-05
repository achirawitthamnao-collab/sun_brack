from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

def run():
    app.run(host="0.0.0.0", port=10000)

def server_on():
    Thread(target=run).start()
