from flask import Blueprint, jsonify, render_template_string, request

import config

main_bp = Blueprint("main", __name__)

_HOME = """
<!doctype html>
<html lang="uk">
<head><meta charset="utf-8"><title>{{ title }}</title></head>
<body>
  <h1>{{ title }}</h1>
  <p>Тип проєкту: <strong>{{ project_type }}</strong></p>
  <p>{{ message }}</p>
  {% if project_type == 'rag' %}
  <form method="post" action="/ask">
    <label>Питання: <input name="question" size="60" required></label>
    <button type="submit">Запитати</button>
  </form>
  {% if answer %}<pre>{{ answer }}</pre>{% endif %}
  {% endif %}
</body>
</html>
"""


@main_bp.route("/")
def index():
    message = (
        "Додайте свій код у student/ (приклади в examples/) і зробіть push — "
        "сайт оновиться автоматично. Оновлення шаблону не перезаписують student/."
    )
    if config.PROJECT_TYPE == "bot":
        message = (
            "Режим Telegram-бота. Сайт лише для деплою; бот працює в Always-on task "
            "(потрібен платний план PythonAnywhere)."
        )
    return render_template_string(
        _HOME,
        title="CSC Template",
        project_type=config.PROJECT_TYPE,
        message=message,
        answer=None,
    )


@main_bp.route("/health")
def health():
    return jsonify({"ok": True, "project_type": config.PROJECT_TYPE})


@main_bp.route("/ask", methods=["POST"])
def ask():
    if config.PROJECT_TYPE != "rag":
        return jsonify({"error": "RAG mode is not enabled"}), 400

    question = (request.form.get("question") or "").strip()
    if not question:
        return jsonify({"error": "empty question"}), 400

    from rag.chain import ask_question

    answer = ask_question(question)
    return render_template_string(
        _HOME,
        title="CSC RAG",
        project_type=config.PROJECT_TYPE,
        message="Приклад RAG. Замініть логіку у student/rag.py або rag/chain.py.",
        answer=answer,
    )
