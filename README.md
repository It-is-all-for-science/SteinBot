# SteinBot — Telegram Bot с AI

## Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd telegram_bot_project
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Настройте переменные окружения:**
   - Создайте файл `.env` по примеру из `env_example.txt` (или настройте переменные окружения на сервере Render):
     - `TELEGRAM_TOKEN` — токен вашего Telegram-бота
     - `RENDER_EXTERNAL_URL` — URL вашего Render-сервиса (например: `https://your-app.onrender.com`)
     - `WEBHOOK_SECRET` — секрет для вебхука (любой строкой)
     - (опционально) `OPENAI_API_KEY`, `HF_API_KEY`, `OR_API_KEY`

5. **Запуск:**
   ```bash
   python bot.py
   ```

## Функционал
- Обработка текстовых, голосовых, изображений и документов
- Интеграция с LLM (OpenAI, HuggingFace, OpenRouter)
- Поддержка команд: `/start`, `/style`, `/ingest`, `/stats`
- Вебхук для продакшена (Render), polling для локальной разработки

## Структура
- `bot.py` — основной файл запуска
- `handlers/` — обработчики команд и сообщений
- `services/` — интеграция с LLM, поиск, голос, загрузка
- `data/` — база знаний

---

**Документация и примеры использования — см. комментарии в коде.**
