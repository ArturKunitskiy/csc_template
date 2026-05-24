"""Скопіюйте як student/bot_handlers.py"""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text or "?")


def register(application: Application) -> None:
    application.add_handler(CommandHandler("echo", echo))
