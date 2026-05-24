"""Shared settings for local run and PythonAnywhere."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# flask | bot | rag
PROJECT_TYPE = os.getenv("PROJECT_TYPE", "flask").strip().lower()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# GitHub → auto-deploy (set the same value in GitHub webhook Secret)
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

# Path to repo on PythonAnywhere (override if you cloned elsewhere)
REPO_PATH = Path(os.getenv("REPO_PATH", str(BASE_DIR)))

# Full path to your WSGI file on PA (for reload after pull)
PA_WSGI_FILE = os.getenv(
    "PA_WSGI_FILE",
    "",  # e.g. /var/www/youruser_pythonanywhere_com_wsgi.py
)

PA_USERNAME = os.getenv("PA_USERNAME", "")
PA_API_TOKEN = os.getenv("PA_API_TOKEN", "")
PA_API_HOST = os.getenv("PA_API_HOST", "www.pythonanywhere.com")
PA_DOMAIN = os.getenv("PA_DOMAIN", "")  # youruser.pythonanywhere.com

# Always-on task id for Telegram bot (create in PA dashboard, then paste id)
PA_ALWAYS_ON_TASK_ID = os.getenv("PA_ALWAYS_ON_TASK_ID", "")
