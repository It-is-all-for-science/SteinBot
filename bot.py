import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers.commands import start, style, ingest, stats
from handlers.messages import handle_text, handle_voice, handle_image, handle_document

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("style", style))
    app.add_handler(CommandHandler("ingest", ingest))
    app.add_handler(CommandHandler("stats", stats))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("SteinBot запущен. Ожидаю сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()