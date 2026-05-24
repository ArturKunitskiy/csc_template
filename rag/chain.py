"""Minimal RAG example (OpenAI). Replace with your logic or student/rag.py."""

from __future__ import annotations

from pathlib import Path

import config

_KNOWLEDGE_DIR = config.REPO_PATH / "student" / "knowledge"
_FALLBACK = (
    "Це демо RAG без векторної БД: контекст — усі .txt файли з student/knowledge/. "
    "Додайте файли і налаштуйте OPENAI_API_KEY."
)


def _load_context() -> str:
    if not _KNOWLEDGE_DIR.is_dir():
        return _FALLBACK
    parts: list[str] = []
    for path in sorted(_KNOWLEDGE_DIR.glob("*.txt")):
        parts.append(f"--- {path.name} ---\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts) if parts else _FALLBACK


def ask_question(question: str) -> str:
    student = config.REPO_PATH / "student" / "rag.py"
    if student.is_file():
        import importlib.util

        spec = importlib.util.spec_from_file_location("student_rag", student)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "ask_question"):
                return module.ask_question(question)

    if not config.OPENAI_API_KEY:
        return "Встановіть OPENAI_API_KEY у змінних середовища PythonAnywhere."

    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    context = _load_context()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Відповідай українською, коротко. Використовуй лише наданий контекст. "
                    "Якщо відповіді немає в контексті — скажи про це."
                ),
            },
            {"role": "user", "content": f"Контекст:\n{context}\n\nПитання: {question}"},
        ],
    )
    return response.choices[0].message.content or ""
