import os
import sys
from dotenv import load_dotenv
print("[DEBUG] Импортированы os, sys, dotenv", flush=True)
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
print("[DEBUG] Импортированы telegram и handlers", flush=True)
from handlers.commands import start, style, ingest, stats
from handlers.messages import handle_text, handle_voice, handle_image, handle_document

print("[DEBUG] Загружаю переменные окружения", flush=True)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", 10000))

print(f"[DEBUG] TOKEN: {bool(TOKEN)}, RENDER_EXTERNAL_URL: {RENDER_EXTERNAL_URL}, PORT: {PORT}", flush=True)

if not TOKEN:
    print("ERROR: TELEGRAM_TOKEN не задан!", flush=True)
    sys.exit(1)

if not RENDER_EXTERNAL_URL:
    print("WARNING: RENDER_EXTERNAL_URL не задан. Бот будет работать в режиме polling для локальной разработки.", flush=True)
    RENDER_EXTERNAL_URL = None

def main():
    print("=== Starting SteinBot ===", flush=True)
    print(f"PORT: {PORT}", flush=True)
    print(f"RENDER_EXTERNAL_URL: {RENDER_EXTERNAL_URL}", flush=True)
    
    tg_app = Application.builder().token(TOKEN).build()
    print("[DEBUG] Application создан", flush=True)

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

    print("All handlers registered successfully", flush=True)

    if RENDER_EXTERNAL_URL:
        # Режим webhook для Render
        webhook_url = f"{RENDER_EXTERNAL_URL}/"
        print(f"Setting webhook: {webhook_url}", flush=True)
        tg_app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
            allowed_updates=Update.ALL_TYPES,
        )
    else:
        # Режим polling для локальной разработки
        print("Starting polling mode for local development...", flush=True)
        tg_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    print("[DEBUG] Запуск main()", flush=True)
    main()