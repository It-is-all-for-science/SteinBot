from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "SteinBot is alive!"

@app.route('/health')
def health():
    return "OK"

# ВАЖНО: Не вызывайте app.run() здесь!
# Flask-сервер должен запускаться только через функцию run() в отдельном потоке из bot.py

def run():
    port = int(os.environ.get("PORT", 10000))  # Render всегда подставляет PORT
    app.run(host="0.0.0.0", port=port)