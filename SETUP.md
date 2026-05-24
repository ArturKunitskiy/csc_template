# Налаштування PythonAnywhere (для студентів)

Мета: **один раз** налаштувати, далі кожен `git push` у ваш форк **автоматично** оновлює код на PythonAnywhere.

## Що потрібно

- Акаунт [PythonAnywhere](https://www.pythonanywhere.com) (безкоштовний підходить для Flask/RAG)
- Форк цього репозиторію на GitHub
- 15–20 хвилин на перше налаштування

## Крок 1. Форк і перший push

1. Натисніть **Fork** на GitHub.
2. Клонуйте **свій** репозиторій. Один раз у репо: `git config merge.ours.driver true` (захист `student/` при оновленнях шаблону).
3. Додайте код у `student/` (приклади копіюйте з `examples/`), зробіть `git push`.

> Оновлення курсу з репозиторію викладача не перезаписують `student/` — див. [docs/SYNC_TEMPLATE.md](docs/SYNC_TEMPLATE.md).

## Крок 2. Клон на PythonAnywhere

1. Увійдіть на PythonAnywhere → **Consoles** → **Bash**.
2. Виконайте (замініть URL на свій форк):

```bash
export GITHUB_REPO="https://github.com/ВАШ_ЛОГІН/csc_template.git"
export PROJECT_DIR="$HOME/csc_template"
git clone "$GITHUB_REPO" "$PROJECT_DIR"
cd "$PROJECT_DIR"
mkvirtualenv --python=python3.10 csc-venv
pip install -r requirements.txt
```

Або запустіть готовий скрипт:

```bash
export GITHUB_REPO="https://github.com/ВАШ_ЛОГІН/csc_template.git"
bash scripts/bootstrap_pythonanywhere.sh
```

## Крок 3. Web app (Flask / RAG / deploy для бота)

1. **Web** → **Add a new web app** → **Manual configuration** → Python **3.10**.
2. **Code** → Source code: `/home/ВАШ_ЛОГІН/csc_template`
3. **Virtualenv**: `/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv`
4. **WSGI configuration file** — замініть вміст на:

```python
import sys

project_home = "/home/ВАШ_ЛОГІН/csc_template"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from wsgi import application
```

5. **Reload** веб-додатку.

## Крок 4. Змінні середовища

**Web** → ваш сайт → **Environment variables** (або файл `.env` локально — на PA краще через dashboard).

Скопіюйте з [.env.example](.env.example). Обов’язково:

| Змінна | Опис |
|--------|------|
| `PROJECT_TYPE` | `flask`, `bot` або `rag` |
| `REPO_PATH` | `/home/ВАШ_ЛОГІН/csc_template` |
| `GITHUB_WEBHOOK_SECRET` | Довгий випадковий рядок |
| `PA_WSGI_FILE` | Шлях до WSGI, напр. `/var/www/вашлогін_pythonanywhere_com_wsgi.py` |

Для RAG: `OPENAI_API_KEY`. Для бота: `TELEGRAM_BOT_TOKEN`.

**Reload** після зміни змінних.

## Крок 5. GitHub webhook (авто-оновлення)

1. GitHub → ваш репозиторій → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `https://ВАШ_ЛОГІН.pythonanywhere.com/deploy-webhook`
3. **Content type**: `application/json`
4. **Secret**: той самий, що `GITHUB_WEBHOOK_SECRET`
5. Події: лише **Just the push event**
6. **Add webhook** — має бути зелена галочка після delivery.

Тепер кожен **push** у `main` (або `master`) робить `git pull` на сервері, `pip install` і reload сайту.

### Опційно: GitHub Actions

Якщо webhook незручний, додайте secrets у репозиторії:

- `DEPLOY_WEBHOOK_URL` = `https://ВАШ_ЛОГІН.pythonanywhere.com/deploy-webhook`
- `GITHUB_WEBHOOK_SECRET` = той самий секрет

Workflow [.github/workflows/deploy.yml](.github/workflows/deploy.yml) дублює виклик після push.

## Режим Telegram-бота

На **безкоштовному** плані бот **не може** працювати 24/7 (немає Always-on). Потрібен мінімум **Hacker** ($5/міс) або запуск бота на іншому хостингу.

1. `PROJECT_TYPE=bot`, `TELEGRAM_BOT_TOKEN=...`
2. Web app залишається для `/deploy-webhook` і `/health`
3. **Tasks** → **Always-on tasks** → команда:

```bash
/home/ВАШ_ЛОГІН/.virtualenvs/csc-venv/bin/python -m bot.main
```

4. Скопіюйте **id** задачі в `PA_ALWAYS_ON_TASK_ID` (для перезапуску після deploy)
5. Додайте `PA_USERNAME`, `PA_API_TOKEN` (Account → API token)

Після push webhook зробить pull і **перезапустить** Always-on через API.

## Режим RAG

1. `PROJECT_TYPE=rag`, `OPENAI_API_KEY=...`
2. Тексти знань — у `student/knowledge/*.txt`
3. Відкрийте сайт → форма «Запитати» або замініть логіку в `student/rag.py`

## Перевірка

```bash
curl https://ВАШ_ЛОГІН.pythonanywhere.com/health
```

Змініть файл у `student/`, `git push` — через 10–30 с оновиться головна сторінка.

## Типові проблеми

| Проблема | Рішення |
|----------|---------|
| 403 на webhook | Secret у GitHub = `GITHUB_WEBHOOK_SECRET` на PA |
| Сайт старий після push | Error log на Web tab; перевірте `REPO_PATH` |
| `git pull` failed | На PA у консолі: `cd ~/csc_template && git status` |
| Бот не відповідає | Always-on увімкнено? Токен вірний? |

## Для викладача

Студенти форкають один шаблон, додають код у `student/`, один раз проходять цей чекліст. Далі workflow однаковий для Flask, RAG і бота (з обмеженням Always-on для бота).

Правила змін у шаблоні, щоб не ламати форки: [MAINTAINERS.md](MAINTAINERS.md).
