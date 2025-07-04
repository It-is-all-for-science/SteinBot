import os
import sys
from dotenv import load_dotenv
print("[DEBUG] Импортированы os, sys, dotenv", flush=True)
from flask import Flask, request
print("[DEBUG] Импортирован Flask", flush=True)
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters
# print("[DEBUG] Импортированы telegram и handlers", flush=True)
# from handlers.commands import start, style, ingest, stats
# from handlers.messages import handle_text, handle_voice, handle_image, handle_document

print("[DEBUG] Загружаю переменные окружения", flush=True)
load_dotenv()
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def root():
    print(f"[DEBUG] Получен {request.method} на /", flush=True)
    return "Flask is alive!", 200

if __name__ == "__main__":
    print(f"[DEBUG] Запуск Flask на порту {PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT)