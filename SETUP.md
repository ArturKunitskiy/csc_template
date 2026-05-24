# PythonAnywhere — налаштування

**Приклад з реального тесту:** акаунт `csctemplate`, сайт https://csctemplate.pythonanywhere.com, панель https://www.pythonanywhere.com/user/csctemplate/ — деталі в [docs/EXAMPLE_CSCTEMPLATE.md](docs/EXAMPLE_CSCTEMPLATE.md). У командах нижче замініть `csctemplate` на **свій** логін.

## Швидко: GUI-майстер (рекомендовано)

На **своєму комп’ютері**:

```bash
python tools/pa_setup_gui.py
```

За замовчуванням підставлено `csctemplate` + `www.pythonanywhere.com`. Змініть логін і URL форку → **Згенерувати** → блок **«1. Bash»** у [Bash-консоль PA](https://www.pythonanywhere.com/user/csctemplate/consoles/) (у вас буде `/user/ВАШ_ЛОГІН/consoles/...`).

---

## 1. Fork і clone на PA

```bash
git clone https://github.com/ВАШ_GITHUB/csc_template.git /home/csctemplate/csc_template
cd /home/csctemplate/csc_template
git config merge.ours.driver true

mkdir -p ~/.virtualenvs
python3.10 -m venv ~/.virtualenvs/csc-venv
source ~/.virtualenvs/csc-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> `mkvirtualenv` на PA часто **не працює** — використовуйте `python3.10 -m venv`.

---

## 2. Web app — усі поля обов’язкові

**Web** → **Add a new web app** → **Manual configuration** → Python **3.10**.

| Поле | Приклад (csctemplate) |
|------|------------------------|
| **Source code** | `/home/csctemplate/csc_template` |
| **Working directory** | `/home/csctemplate/csc_template` |
| **Virtualenv** | `/home/csctemplate/.virtualenvs/csc-venv` |

**WSGI configuration file**:

```python
import sys
sys.path.insert(0, "/home/csctemplate/csc_template")
from wsgi import application
```

**Reload** → перевірка: https://csctemplate.pythonanywhere.com/health

---

## 3. Змінні середовища

**Web** → Environment variables (зразок у [.env.example](.env.example)):

```text
REPO_PATH=/home/csctemplate/csc_template
GITHUB_WEBHOOK_SECRET=<ваш_секрет>
PA_WSGI_FILE=/var/www/csctemplate_pythonanywhere_com_wsgi.py
PA_USERNAME=csctemplate
PA_API_HOST=www.pythonanywhere.com
PA_DOMAIN=csctemplate.pythonanywhere.com
```

API-ключі студента: [docs/TOKENS.md](docs/TOKENS.md). Після змін — **Reload**.

---

## 4. GitHub webhook

| Поле | Приклад (csctemplate) |
|------|------------------------|
| Payload URL | `https://csctemplate.pythonanywhere.com/deploy-webhook` |
| Secret | = `GITHUB_WEBHOOK_SECRET` |
| Events | push |

---

## 5. Код у `students/`

```python
from config import get_token

def register(app):
    @app.route("/me")
    def me():
        return "Мій проєкт"
```

`git push` → оновлення на PA.

---

## Telegram-бот

[docs/TELEGRAM_PA.md](docs/TELEGRAM_PA.md) · приклад `students/_example_bot.py` → `students/bot.py`

Always-on:

```bash
/home/csctemplate/.virtualenvs/csc-venv/bin/python /home/csctemplate/csc_template/run_students.py
```

`PA_API_HOST=www.pythonanywhere.com` — як у тестовому акаунті на **www**, не eu.
