# Синхронізація з оновленнями шаблону (без поломки `student/`)

## Як це влаштовано

1. **Ваш код** — тільки в `student/` (і власні коміти в інших місцях, якщо потрібно).
2. **Шаблон курсу** оновлює `app/`, `bot/`, `deploy`, `SETUP.md` тощо — **не чіпає** ваші файли в `student/`.
3. У [`.gitattributes`](../.gitattributes) для `student/**` увімкнено **`merge=ours`**: при злитті з upstream конфлікти в цій папці вирішуються на користь **вашої** гілки.

Приклади й демо-дані лежать у `examples/`, а не в `student/` — їх можна копіювати вручну, коли потрібно.

## Один раз: драйвер злиття (після клону форку)

```bash
git config merge.ours.driver true
```

Без цього рядка `.gitattributes` для `student/**` може не спрацювати.

## Один раз: підключити upstream

Замініть URL на репозиторій викладача:

```bash
git remote add upstream https://github.com/ВИКЛАДАЧ/csc_template.git
git fetch upstream
```

## Оновити форк з шаблону

```bash
bash scripts/sync_from_template.sh
```

Або вручну:

```bash
git fetch upstream
git merge upstream/main -m "Sync template updates"
# якщо основна гілка називається master:
# git merge upstream/master -m "Sync template updates"
git push origin main
```

Після merge перевірте сайт на PythonAnywhere (звичайний `git push` уже оновить сервер).

## Якщо з’явилися конфлікти поза `student/`

Git покаже файли на кшталт `app/deploy.py`. Відкрийте їх, злийте зміни шаблону зі своїми правками (якщо ви щось міняли в ядрі), потім:

```bash
git add .
git commit
git push
```

Файли в `student/` при цьому **не повинні** перезаписуватися шаблоном.

## Для викладача

Правила оновлення шаблону: [MAINTAINERS.md](../MAINTAINERS.md).
