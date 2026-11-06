"""Flask application factory for TaskFlow."""

import os
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from .database import close_db, init_db
from .tasks import tasks_bp

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def create_app(test_config: dict | None = None) -> Flask:
    """Create a configured application and initialize its database schema."""
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path="/static",
    )

    default_database = PROJECT_ROOT / "instance" / "taskflow.sqlite3"
    app.config.from_mapping(
        DATABASE=os.environ.get("DATABASE_PATH", str(default_database)),
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=32 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    database_path = app.config["DATABASE"]
    if database_path != ":memory:":
        Path(database_path).expanduser().resolve().parent.mkdir(
            parents=True, exist_ok=True
        )

    app.teardown_appcontext(close_db)
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    with app.app_context():
        init_db()

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "TaskFlow API"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Không tìm thấy tài nguyên."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Phương thức HTTP không được hỗ trợ."}), 405

    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify({"error": "Dữ liệu gửi lên vượt quá giới hạn cho phép."}), 413

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "Đã xảy ra lỗi máy chủ."}), 500

    return app
