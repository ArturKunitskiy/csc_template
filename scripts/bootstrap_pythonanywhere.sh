#!/usr/bin/env bash
# Одноразове налаштування на PythonAnywhere (Bash console).
# Перед запуском: замініть GITHUB_REPO на URL форку студента.

set -euo pipefail

GITHUB_REPO="${GITHUB_REPO:-https://github.com/YOUR_USER/csc_template.git}"
PROJECT_DIR="${PROJECT_DIR:-$HOME/csc_template}"
VENV_DIR="${VENV_DIR:-$HOME/.virtualenvs/csc-venv}"

echo "==> Clone"
if [[ ! -d "$PROJECT_DIR/.git" ]]; then
  git clone "$GITHUB_REPO" "$PROJECT_DIR"
else
  echo "Already cloned: $PROJECT_DIR"
fi

cd "$PROJECT_DIR"

echo "==> Virtualenv"
if [[ ! -d "$VENV_DIR" ]]; then
  mkvirtualenv --python=python3.10 csc-venv
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

echo "==> post-merge hook (reload after manual git pull)"
HOOK="$PROJECT_DIR/.git/hooks/post-merge"
cat > "$HOOK" <<'HOOK_EOF'
#!/bin/sh
# Reload web app when you git pull in console
touch "${PA_WSGI_FILE:-/var/www/__REPLACE_ME___wsgi.py}" 2>/dev/null || true
HOOK_EOF
chmod +x "$HOOK"

echo ""
echo "Далі вручну (Web tab → Add a new web app):"
echo "  1. Manual configuration, Python 3.10"
echo "  2. Source code: $PROJECT_DIR"
echo "  3. Virtualenv: $VENV_DIR"
echo "  4. WSGI file: $PROJECT_DIR/wsgi.py  (або вкажіть application у стандартному wsgi)"
echo "  5. Account → API token → скопіюйте в .env / Environment variables"
echo "  6. Web → Environment variables (див. .env.example)"
echo "  7. GitHub → Settings → Webhooks → URL:"
echo "       https://YOURUSER.pythonanywhere.com/deploy-webhook"
echo "     Secret = GITHUB_WEBHOOK_SECRET"
echo ""
