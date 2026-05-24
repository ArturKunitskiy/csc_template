# Правила оновлення шаблону (для викладача)

## Не змінювати у наступних релізах

- Будь-які файли в `student/`, крім `.gitkeep`, `.workspace` (одноразові маркери).
- Не додавати в `student/` нові обов’язкові файли — лише в `examples/` або `docs/`.

Студенти кладуть код у `student/`; злиття з upstream для цієї папки захищено через `.gitattributes` (`merge=ours`).

## Де вносити зміни шаблону

| Що оновлюєте | Куди |
|--------------|------|
| Flask, deploy, RAG, bot | `app/`, `bot/`, `rag/`, `wsgi.py`, `config.py` |
| Залежності | `requirements.txt` |
| Інструкції | `SETUP.md`, `README.md`, `docs/` |
| Нові приклади для студентів | `examples/` |
| Опис папки student | `docs/student-workspace.md` |

## Нові опційні файли для студентів

1. Додайте приклад у `examples/`.
2. Опишіть у `docs/student-workspace.md`.
3. Не комітьте готовий `student/routes.py` у шаблон — студент копіює сам.

## Перевірка перед push у шаблон

```bash
git diff --name-only origin/main | grep '^student/' || echo "OK: student/ not changed"
```

(або порівняйте з попереднім тегом)
