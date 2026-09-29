from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.core.database import get_session
from app.main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(engine)


def get_test_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


def test_create_task():
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Complete HNG Stage 1",
            "description": "Build the To-Do application",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete HNG Stage 1"
    assert data["description"] == "Build the To-Do application"
    assert data["priority"] == "high"
    assert data["completed"] is False


def test_list_tasks():
    client.post(
        "/api/v1/tasks",
        json={"title": "Task One", "priority": "low"},
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Task Two", "priority": "high"},
    )

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_list_tasks_by_priority():
    client.post(
        "/api/v1/tasks",
        json={"title": "High Priority Task", "priority": "high"},
    )

    response = client.get("/api/v1/tasks?priority=high")

    assert response.status_code == 200
    assert all(task["priority"] == "high" for task in response.json())


def test_get_task():
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Find this task", "priority": "medium"},
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Find this task"


def test_get_task_not_found():
    response = client.get("/api/v1/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original title", "priority": "low"},
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated title", "priority": "high"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["priority"] == "high"


def test_update_task_not_found():
    response = client.put(
        "/api/v1/tasks/999999",
        json={"title": "Updated title"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task():
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task to delete", "priority": "low"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    response = client.delete("/api/v1/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
