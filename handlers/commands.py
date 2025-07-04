import time
from telegram import Update
from telegram.ext import ContextTypes

PERSONALITIES = {
    "postdoc": "Саркастичный постдок",
    "reviewer2": "Пассивно-агрессивный рецензент №2",
    "student": "Наивный студент"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] start: start", flush=True)
    start_time = time.time()
    try:
        await update.message.reply_text(
            "Я SteinBot — научный рецензент с характером.\n"
            "Загрузи статью (.txt, .docx, .pdf) или отправь вопрос.\n"
            "Сменить стиль: /style <postdoc|reviewer2|student>"
        )
    except Exception as e:
        print(f"[ERROR] start: {e}", flush=True)
    print(f"[DEBUG] start: end, elapsed={time.time() - start_time:.2f}s", flush=True)

async def style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] style: start, text={getattr(update.message, 'text', None)}", flush=True)
    start_time = time.time()
    try:
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
    except Exception as e:
        print(f"[ERROR] style: {e}", flush=True)
    print(f"[DEBUG] style: end, elapsed={time.time() - start_time:.2f}s", flush=True)

async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] ingest: start", flush=True)
    start_time = time.time()
    try:
        from services.loader import ingest_all
        ingest_all()
        await update.message.reply_text("База знаний обновлена!")
    except Exception as e:
        print(f"[ERROR] ingest: {e}", flush=True)
    print(f"[DEBUG] ingest: end, elapsed={time.time() - start_time:.2f}s", flush=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] stats: start", flush=True)
    start_time = time.time()
    try:
        await update.message.reply_text("Здесь будет статистика (реализуйте по желанию).")
    except Exception as e:
        print(f"[ERROR] stats: {e}", flush=True)
    print(f"[DEBUG] stats: end, elapsed={time.time() - start_time:.2f}s", flush=True)