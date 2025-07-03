import os
import sys
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.commands import start, style, ingest, stats
from handlers.messages import handle_text, handle_voice, handle_image, handle_document

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    print("ERROR: TELEGRAM_TOKEN не задан!")
    sys.exit(1)

if not RENDER_EXTERNAL_URL:
    print("WARNING: RENDER_EXTERNAL_URL не задан. Бот будет работать в режиме polling для локальной разработки.")
    RENDER_EXTERNAL_URL = None

app = Flask(__name__)
tg_app = None

@app.route("/", methods=["GET"])
def home():
    return "SteinBot is alive!"

@app.route("/health", methods=["GET"])
def health():
    return "OK"

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), tg_app.bot)
            tg_app.update_queue.put(update)
            return "OK"
        except Exception as e:
            print(f"Webhook error: {e}")
            return "Error", 500
    return "Not allowed", 405

def main():
    global tg_app
    print("=== Starting SteinBot ===")
    print(f"PORT: {PORT}")
    print(f"RENDER_EXTERNAL_URL: {RENDER_EXTERNAL_URL}")
    
    tg_app = Application.builder().token(TOKEN).build()

    # Команды
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CommandHandler("style", style))
    tg_app.add_handler(CommandHandler("ingest", ingest))
    tg_app.add_handler(CommandHandler("stats", stats))

    # Сообщения
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    tg_app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    tg_app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    tg_app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("All handlers registered successfully")

    if RENDER_EXTERNAL_URL:
        # Режим webhook для Render
        webhook_url = f"{RENDER_EXTERNAL_URL}/webhook/{WEBHOOK_SECRET}"
        print(f"Setting webhook: {webhook_url}")
        tg_app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
            allowed_updates=Update.ALL_TYPES,
        )
    else:
        # Режим polling для локальной разработки
        print("Starting polling mode for local development...")
        tg_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()