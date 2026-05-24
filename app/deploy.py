"""GitHub webhook: git pull on push + reload webapp / restart bot."""

from __future__ import annotations

import hashlib
import hmac
import logging
import subprocess
from pathlib import Path

import requests
from flask import Blueprint, abort, request

import config

logger = logging.getLogger(__name__)

deploy_bp = Blueprint("deploy", __name__)


def _verify_github_signature(payload: bytes, signature_header: str | None) -> bool:
    secret = config.GITHUB_WEBHOOK_SECRET
    if not secret:
        logger.warning("GITHUB_WEBHOOK_SECRET is not set — deploy webhook disabled")
        return False
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = (
        "sha256="
        + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    )
    return hmac.compare_digest(expected, signature_header)


def _run(cmd: list[str], cwd: Path) -> None:
    logger.info("Running %s in %s", cmd, cwd)
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _git_pull() -> None:
    repo = config.REPO_PATH
    _run(["git", "fetch", "origin"], repo)
    for branch in ("main", "master"):
        try:
            _run(["git", "checkout", branch], repo)
            _run(["git", "pull", "origin", branch], repo)
            return
        except subprocess.CalledProcessError:
            continue
    raise subprocess.CalledProcessError(1, "git pull", "", "No main/master branch")


def _pip_install() -> None:
    req = config.REPO_PATH / "requirements.txt"
    if req.is_file():
        _run(["pip", "install", "-r", str(req)], config.REPO_PATH)


def _reload_webapp() -> None:
    wsgi = config.PA_WSGI_FILE
    if wsgi:
        Path(wsgi).touch()
        logger.info("Touched WSGI file %s", wsgi)
        return

    if not (config.PA_USERNAME and config.PA_API_TOKEN and config.PA_DOMAIN):
        logger.info("PA API reload skipped (set PA_USERNAME, PA_API_TOKEN, PA_DOMAIN)")
        return

    url = (
        f"https://{config.PA_API_HOST}/api/v0/user/"
        f"{config.PA_USERNAME}/webapps/{config.PA_DOMAIN}/reload/"
    )
    response = requests.post(
        url,
        headers={"Authorization": f"Token {config.PA_API_TOKEN}"},
        timeout=60,
    )
    response.raise_for_status()
    logger.info("Webapp reloaded via API")


def _restart_always_on() -> None:
    task_id = config.PA_ALWAYS_ON_TASK_ID
    if not task_id or not (config.PA_USERNAME and config.PA_API_TOKEN):
        return
    url = (
        f"https://{config.PA_API_HOST}/api/v0/user/"
        f"{config.PA_USERNAME}/always_on/{task_id}/restart/"
    )
    response = requests.post(
        url,
        headers={"Authorization": f"Token {config.PA_API_TOKEN}"},
        timeout=60,
    )
    response.raise_for_status()
    logger.info("Always-on task %s restarted", task_id)


def _apply_student_hooks() -> None:
    """Optional student/deploy_hook.py after pull."""
    hook = config.REPO_PATH / "student" / "deploy_hook.py"
    if not hook.is_file():
        return
    import importlib.util

    spec = importlib.util.spec_from_file_location("student_deploy_hook", hook)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "after_deploy"):
            module.after_deploy()


@deploy_bp.route("/deploy-webhook", methods=["POST"])
def deploy_webhook():
    if not _verify_github_signature(
        request.data, request.headers.get("X-Hub-Signature-256")
    ):
        abort(403)

    event = request.headers.get("X-GitHub-Event", "")
    if event == "ping":
        return "", 204
    if event != "push":
        return "ignored", 200

    try:
        _git_pull()
        _pip_install()
        _apply_student_hooks()
        _reload_webapp()
        if config.PROJECT_TYPE == "bot":
            _restart_always_on()
    except subprocess.CalledProcessError as exc:
        logger.exception("Deploy failed")
        return (exc.stderr or str(exc)), 500

    return "deployed", 200
