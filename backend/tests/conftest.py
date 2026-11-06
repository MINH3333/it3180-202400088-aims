"""Shared pytest fixtures for API tests."""

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test_taskflow.sqlite3"
    application = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
        }
    )
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


def create_sample_task(client, **overrides):
    payload = {"title": "Ôn tập Công nghệ phần mềm", "description": "Viết unit test"}
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.json
