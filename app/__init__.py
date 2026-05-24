from flask import Flask

import config
from app.deploy import deploy_bp
from app.routes import main_bp


def _register_student_routes(app: Flask) -> None:
    hook = config.REPO_PATH / "student" / "routes.py"
    if not hook.is_file():
        return
    import importlib.util

    spec = importlib.util.spec_from_file_location("student_routes", hook)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "register"):
            module.register(app)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(deploy_bp)
    _register_student_routes(app)

    @app.context_processor
    def inject_project_type():
        return {"project_type": config.PROJECT_TYPE}

    return app
