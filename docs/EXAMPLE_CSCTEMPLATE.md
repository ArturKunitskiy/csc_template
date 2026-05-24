# Приклад: акаунт csctemplate (перевірено на PA)

Реальні URL з тестового налаштування. У своєму форку **замініть `csctemplate` на свій логін**.

| Що | Значення |
|----|----------|
| Вхід / панель | https://www.pythonanywhere.com/user/csctemplate/ |
| Bash-консоль (приклад) | https://www.pythonanywhere.com/user/csctemplate/consoles/46886841/ |
| Сайт | https://csctemplate.pythonanywhere.com |
| Health | https://csctemplate.pythonanywhere.com/health |
| Webhook | https://csctemplate.pythonanywhere.com/deploy-webhook |
| **PA_API_HOST** | `www.pythonanywhere.com` (не `eu` — акаунт на www) |

## Шляхи на сервері

```text
/home/csctemplate/csc_template              # код (REPO_PATH)
/home/csctemplate/.virtualenvs/csc-venv     # virtualenv
/var/www/csctemplate_pythonanywhere_com_wsgi.py   # PA_WSGI_FILE
```

## Клон (приклад форку)

```bash
git clone https://github.com/ВАШ_GITHUB/csc_template.git /home/csctemplate/csc_template
```

## WSGI (фрагмент у Web tab)

```python
import sys
sys.path.insert(0, "/home/csctemplate/csc_template")
from wsgi import application
```

## Always-on (бот)

```bash
/home/csctemplate/.virtualenvs/csc-venv/bin/python /home/csctemplate/csc_template/run_students.py
```

GUI-майстер за замовчуванням підставляє ці значення — змініть лише логін і URL GitHub.
