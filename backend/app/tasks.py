"""REST endpoints and input validation for TaskFlow tasks."""

import sqlite3
from typing import Any

from flask import Blueprint, jsonify, request

from .database import get_db

tasks_bp = Blueprint("tasks", __name__)
ALLOWED_FIELDS = {"title", "description", "completed"}


def _serialize_task(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a SQLite row into the public JSON representation."""
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _validate_text(
    value: Any,
    field: str,
    max_length: int,
    *,
    required: bool = False,
) -> tuple[str | None, str | None]:
    """Validate and normalize a text value."""
    if value is None:
        if required:
            return None, f"Trường '{field}' là bắt buộc."
        return None, f"Trường '{field}' phải là chuỗi."
    if not isinstance(value, str):
        return None, f"Trường '{field}' phải là chuỗi."

    cleaned = value.strip()
    if required and not cleaned:
        return None, f"Trường '{field}' không được để trống."
    if len(cleaned) > max_length:
        return None, f"Trường '{field}' không được vượt quá {max_length} ký tự."
    return cleaned, None


def _read_json_object():
    """Return a JSON object or a consistent client error response."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, (jsonify({"error": "Dữ liệu gửi lên phải là JSON object."}), 400)

    unknown_fields = set(payload) - ALLOWED_FIELDS
    if unknown_fields:
        fields = ", ".join(sorted(unknown_fields))
        return None, (
            jsonify({"error": f"Trường không được hỗ trợ: {fields}."}),
            400,
        )
    return payload, None


@tasks_bp.get("")
def list_tasks():
    rows = get_db().execute(
        "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
    ).fetchall()
    return jsonify([_serialize_task(row) for row in rows])


@tasks_bp.post("")
def create_task():
    payload, error_response = _read_json_object()
    if error_response:
        return error_response

    title, error = _validate_text(
        payload.get("title"), "title", 120, required=True
    )
    if error:
        return jsonify({"error": error}), 400

    description, error = _validate_text(
        payload.get("description", ""), "description", 1000
    )
    if error:
        return jsonify({"error": error}), 400

    completed = payload.get("completed", False)
    if not isinstance(completed, bool):
        return jsonify({"error": "Trường 'completed' phải là true hoặc false."}), 400

    connection = get_db()
    cursor = connection.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (title, description, int(completed)),
    )
    connection.commit()
    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(_serialize_task(row)), 201


@tasks_bp.get("/<int:task_id>")
def get_task(task_id: int):
    row = get_db().execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "Không tìm thấy công việc."}), 404
    return jsonify(_serialize_task(row))


@tasks_bp.patch("/<int:task_id>")
def update_task(task_id: int):
    payload, error_response = _read_json_object()
    if error_response:
        return error_response
    if not payload:
        return jsonify({"error": "Hãy gửi ít nhất một trường cần cập nhật."}), 400

    connection = get_db()
    existing = connection.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if existing is None:
        return jsonify({"error": "Không tìm thấy công việc."}), 404

    title = existing["title"]
    description = existing["description"]
    completed = bool(existing["completed"])

    if "title" in payload:
        title, error = _validate_text(
            payload["title"], "title", 120, required=True
        )
        if error:
            return jsonify({"error": error}), 400

    if "description" in payload:
        description, error = _validate_text(
            payload["description"], "description", 1000
        )
        if error:
            return jsonify({"error": error}), 400

    if "completed" in payload:
        if not isinstance(payload["completed"], bool):
            return jsonify({"error": "Trường 'completed' phải là true hoặc false."}), 400
        completed = payload["completed"]

    connection.execute(
        """UPDATE tasks
           SET title = ?, description = ?, completed = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (title, description, int(completed), task_id),
    )
    connection.commit()
    updated = connection.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    return jsonify(_serialize_task(updated))


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id: int):
    connection = get_db()
    cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Không tìm thấy công việc."}), 404
    return jsonify({"message": "Đã xóa công việc."}), 200
