# csc_template

Шаблон курсу: форк → код у `student/` → push → **автоматичний деплой** на [PythonAnywhere](https://www.pythonanywhere.com).

## Режими

| `PROJECT_TYPE` | Що це |
|----------------|--------|
| `flask` | Веб-сайт (за замовчуванням) |
| `rag` | Flask + приклад RAG (OpenAI) |
| `bot` | Telegram-бот (Always-on на PA) + сайт для деплою |

## Швидкий старт

1. **Fork** репозиторію
2. Детальна інструкція: **[SETUP.md](SETUP.md)**
3. Ваш код — лише в **`student/`** (приклади в `examples/`, опис у [docs/student-workspace.md](docs/student-workspace.md))
4. Оновлення шаблону без втрати роботи: **[docs/SYNC_TEMPLATE.md](docs/SYNC_TEMPLATE.md)**
5. Локально: `cp .env.example .env` → `pip install -r requirements.txt` → `python run_local.py`

## Структура

```
app/           Flask + /deploy-webhook
bot/           Telegram bot (python -m bot.main)
rag/           Приклад RAG
student/       ← сюди додаєте свій код (захищено merge=ours)
examples/      Приклади для копіювання
docs/          Інструкції, синхронізація з шаблоном
scripts/       bootstrap для PythonAnywhere
```

## Автодеплой

Після push у `main`/`master`:

1. GitHub викликає `POST /deploy-webhook`
2. На сервері: `git pull` → `pip install` → reload сайту (і restart бота, якщо `PROJECT_TYPE=bot`)

Секрет: `GITHUB_WEBHOOK_SECRET` (GitHub webhook + змінні середовища на PA).

## Ліцензія

Навчальний шаблон — використовуйте вільно у курсі.
