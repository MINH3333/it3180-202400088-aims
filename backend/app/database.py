"""SQLite connection and schema management."""

import sqlite3
from pathlib import Path

from flask import current_app, g

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def get_db() -> sqlite3.Connection:
    """Return one SQLite connection for the current application context."""
    if "db" not in g:
        connection = sqlite3.connect(
            current_app.config["DATABASE"],
            timeout=5.0,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    """Close the context-local database connection, if it exists."""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    """Create database tables when the application starts."""
    connection = get_db()
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    connection.commit()
