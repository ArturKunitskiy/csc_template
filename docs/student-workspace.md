# Папка `student/` — ваш код

Покладіть сюди файли проєкту. Після `git push` PythonAnywhere оновиться автоматично (якщо налаштовано webhook).

| Режим | Файли |
|-------|--------|
| Flask | `student/routes.py` — функція `register(app)` |
| Bot | `student/bot_handlers.py` — функція `register(application)` |
| RAG | `student/knowledge/*.txt` та/або `student/rag.py` |
| Будь-який | `student/deploy_hook.py` — функція `after_deploy()` після pull |

Приклади для копіювання — у [`examples/`](../examples/).

Оновлення шаблону курсу **не повинні ламати** ваші файли: у репозиторії налаштовано `merge=ours` для `student/**`. Деталі: [SYNC_TEMPLATE.md](SYNC_TEMPLATE.md).
