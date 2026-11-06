"""API tests covering success paths, validation and not-found cases."""

def create_sample_task(client, **overrides):
    payload = {"title": "Ôn tập Công nghệ phần mềm", "description": "Viết unit test"}
    payload.update(overrides)
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    return response.json


def test_home_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "service": "TaskFlow API"}


def test_list_tasks_is_empty_initially(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json == []


def test_create_task_returns_created_resource(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Hoàn thành bài tập", "description": "Viết kiểm thử API"},
    )
    assert response.status_code == 201
    assert response.json["id"] == 1
    assert response.json["title"] == "Hoàn thành bài tập"
    assert response.json["description"] == "Viết kiểm thử API"
    assert response.json["completed"] is False
    assert "created_at" in response.json
    assert "updated_at" in response.json


def test_create_task_trims_text(client):
    response = client.post("/api/tasks", json={"title": "  Ôn thi  ", "description": "  ghi chú  "})
    assert response.status_code == 201
    assert response.json["title"] == "Ôn thi"
    assert response.json["description"] == "ghi chú"


def test_create_task_can_start_completed(client):
    response = client.post("/api/tasks", json={"title": "Đã xong", "completed": True})
    assert response.status_code == 201
    assert response.json["completed"] is True


def test_create_task_rejects_missing_json(client):
    response = client.post("/api/tasks", data="not-json", content_type="application/json")
    assert response.status_code == 400


def test_create_task_rejects_non_object_json(client):
    response = client.post("/api/tasks", json=["not", "an", "object"])
    assert response.status_code == 400


def test_create_task_requires_title(client):
    response = client.post("/api/tasks", json={"description": "Thiếu tiêu đề"})
    assert response.status_code == 400
    assert "title" in response.json["error"]


def test_create_task_rejects_blank_title(client):
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_create_task_rejects_non_string_title(client):
    response = client.post("/api/tasks", json={"title": 123})
    assert response.status_code == 400


def test_create_task_rejects_title_over_limit(client):
    response = client.post("/api/tasks", json={"title": "x" * 121})
    assert response.status_code == 400


def test_create_task_rejects_description_over_limit(client):
    response = client.post("/api/tasks", json={"title": "Hợp lệ", "description": "x" * 1001})
    assert response.status_code == 400


def test_create_task_rejects_invalid_completed_value(client):
    response = client.post("/api/tasks", json={"title": "Công việc", "completed": "yes"})
    assert response.status_code == 400


def test_create_task_rejects_unknown_fields(client):
    response = client.post("/api/tasks", json={"title": "Công việc", "admin": True})
    assert response.status_code == 400
    assert "admin" in response.json["error"]


def test_get_task_returns_created_task(client):
    task = create_sample_task(client)
    response = client.get(f"/api/tasks/{task['id']}")
    assert response.status_code == 200
    assert response.json["title"] == task["title"]


def test_list_tasks_returns_all_tasks(client):
    create_sample_task(client, title="Công việc A")
    create_sample_task(client, title="Công việc B")
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {task["title"] for task in response.json} == {"Công việc A", "Công việc B"}


def test_patch_task_updates_completion(client):
    task = create_sample_task(client)
    response = client.patch(f"/api/tasks/{task['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json["completed"] is True
    assert response.json["title"] == task["title"]


def test_patch_task_updates_multiple_fields(client):
    task = create_sample_task(client)
    response = client.patch(
        f"/api/tasks/{task['id']}",
        json={"title": "Tên mới", "description": "Mô tả mới", "completed": True},
    )
    assert response.status_code == 200
    assert response.json["title"] == "Tên mới"
    assert response.json["description"] == "Mô tả mới"
    assert response.json["completed"] is True


def test_patch_task_rejects_empty_payload(client):
    task = create_sample_task(client)
    response = client.patch(f"/api/tasks/{task['id']}", json={})
    assert response.status_code == 400


def test_patch_task_rejects_blank_title(client):
    task = create_sample_task(client)
    response = client.patch(f"/api/tasks/{task['id']}", json={"title": " "})
    assert response.status_code == 400


def test_patch_task_rejects_invalid_boolean(client):
    task = create_sample_task(client)
    response = client.patch(f"/api/tasks/{task['id']}", json={"completed": 1})
    assert response.status_code == 400


def test_patch_task_rejects_unknown_fields(client):
    task = create_sample_task(client)
    response = client.patch(f"/api/tasks/{task['id']}", json={"unexpected": "value"})
    assert response.status_code == 400


def test_get_missing_task_returns_404(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_patch_missing_task_returns_404(client):
    response = client.patch("/api/tasks/999", json={"completed": True})
    assert response.status_code == 404


def test_delete_task_removes_resource(client):
    task = create_sample_task(client)
    response = client.delete(f"/api/tasks/{task['id']}")
    assert response.status_code == 200
    assert client.get(f"/api/tasks/{task['id']}").status_code == 404


def test_delete_missing_task_returns_404(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404


def test_create_task_rejects_null_description(client):
    response = client.post("/api/tasks", json={"title": "Hợp lệ", "description": None})
    assert response.status_code == 400


def test_unsupported_method_returns_json_405(client):
    response = client.put("/api/tasks/1", json={"completed": True})
    assert response.status_code == 405
    assert "error" in response.json
