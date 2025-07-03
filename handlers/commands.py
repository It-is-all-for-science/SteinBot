from telegram import Update
from telegram.ext import ContextTypes

PERSONALITIES = {
    "postdoc": "Саркастичный постдок",
    "reviewer2": "Пассивно-агрессивный рецензент №2",
    "student": "Наивный студент"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я SteinBot — научный рецензент с характером.\n"
        "Загрузи статью (.txt, .docx, .pdf) или отправь вопрос.\n"
        "Сменить стиль: /style <postdoc|reviewer2|student>"
    )

async def style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args and args[0] in PERSONALITIES:
        context.user_data["style"] = args[0]
        await update.message.reply_text(f"Стиль рецензента установлен: {PERSONALITIES[args[0]]}")
    else:
        styles = ', '.join(PERSONALITIES.keys())
        await update.message.reply_text(
            f"Доступные стили: {styles}\n"
            "Используй /style <название>"
        )

async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from services.loader import ingest_all
    ingest_all()
    await update.message.reply_text("База знаний обновлена!")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здесь будет статистика (реализуйте по желанию).")