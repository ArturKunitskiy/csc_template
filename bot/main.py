"""Telegram bot entry point for PythonAnywhere Always-on task.

Command on PA (Always-on):
  python -m bot.main
"""

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привіт! Це шаблон бота. Додайте хендлери у student/bot_handlers.py."
    )


def _register_student_handlers(application: Application) -> None:
    hook = config.REPO_PATH / "student" / "bot_handlers.py"
    if not hook.is_file():
        return
    import importlib.util

    spec = importlib.util.spec_from_file_location("student_bot_handlers", hook)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "register"):
            module.register(application)


def main() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    _register_student_handlers(app)
    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
