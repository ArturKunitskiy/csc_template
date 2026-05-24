"""PythonAnywhere WSGI entry point."""

import sys
from pathlib import Path

# Project root on sys.path (PA often uses a separate virtualenv)
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app

application = create_app()
