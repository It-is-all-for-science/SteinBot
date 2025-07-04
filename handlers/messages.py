from telegram import Update
from telegram.ext import ContextTypes
import tempfile
import os
import time
import asyncio

from services.loader import extract_text, ingest_all, search_context
from services.llm import generate_response
from services.voice import transcribe_voice

import base64

# --- Текстовые сообщения ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] handle_text: start, text={getattr(update.message, 'text', None)}", flush=True)
    start = time.time()
    try:
        user_message = update.message.text
        style = context.user_data.get("style", "postdoc")
        loop = asyncio.get_running_loop()
        context_text = await loop.run_in_executor(None, search_context, user_message)
        answer = await loop.run_in_executor(
            None,
            generate_response,
            user_message,
            context_text,
            style
        )
        await update.message.reply_text(answer)
    except Exception as e:
        print(f"[ERROR] handle_text: {e}", flush=True)
    print(f"[DEBUG] handle_text: end, elapsed={time.time() - start:.2f}s", flush=True)

# --- Голосовые сообщения ---
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] handle_voice: start", flush=True)
    start = time.time()
    try:
        voice = await update.message.voice.get_file()
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tf:
            await voice.download_to_drive(tf.name)
            loop = asyncio.get_running_loop()
            text = await loop.run_in_executor(None, transcribe_voice, tf.name)
            os.remove(tf.name)
        style = context.user_data.get("style", "postdoc")
        context_text = await loop.run_in_executor(None, search_context, text)
        answer = await loop.run_in_executor(
            None,
            generate_response,
            text,
            context_text,
            style
        )
        await update.message.reply_text(f"Распознано: {text}\n\n{answer}")
    except Exception as e:
        print(f"[ERROR] handle_voice: {e}", flush=True)
    print(f"[DEBUG] handle_voice: end, elapsed={time.time() - start:.2f}s", flush=True)

# --- Изображения ---
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] handle_image: start", flush=True)
    start = time.time()
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
            await file.download_to_drive(tf.name)
            image_path = tf.name
        with open(image_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        os.remove(image_path)
        style = context.user_data.get("style", "postdoc")
        prompt = (
            "Проанализируй это изображение как научный рецензент. "
            "Оцени корректность, стиль, смысловую нагрузку, укажи возможные ошибки."
        )
        loop = asyncio.get_running_loop()
        answer = await loop.run_in_executor(
            None,
            generate_response,
            prompt,
            "",
            style,
            None,
            img_b64
        )
        await update.message.reply_text(answer)
    except Exception as e:
        print(f"[ERROR] handle_image: {e}", flush=True)
    print(f"[DEBUG] handle_image: end, elapsed={time.time() - start:.2f}s", flush=True)

# --- Документы (PDF, DOCX, TXT и др.) ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] handle_document: start", flush=True)
    start = time.time()
    try:
        document = update.message.document
        file_name = document.file_name
        file = await document.get_file()
        suffix = os.path.splitext(file_name)[-1]
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tf:
            await file.download_to_drive(tf.name)
            temp_path = tf.name
        try:
            loop = asyncio.get_running_loop()
            text = await loop.run_in_executor(None, extract_text, temp_path)
            docs_dir = "docs"
            os.makedirs(docs_dir, exist_ok=True)
            dest_path = os.path.join(docs_dir, file_name)
            os.replace(temp_path, dest_path)
            await loop.run_in_executor(None, ingest_all, docs_dir)
            await update.message.reply_text("Документ загружен и проиндексирован!\nТеперь вы можете задавать вопросы по его содержимому.")
        except Exception as e:
            await update.message.reply_text(f"Ошибка при обработке документа: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception as e:
        print(f"[ERROR] handle_document: {e}", flush=True)
    print(f"[DEBUG] handle_document: end, elapsed={time.time() - start:.2f}s", flush=True)