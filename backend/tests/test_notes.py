from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

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


def create_test_task():
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Task with notes", "priority": "medium"},
    )
    return response.json()["id"]


def test_create_and_list_notes():
    task_id = create_test_task()

    create_response = client.post(
        f"/api/v1/tasks/{task_id}/notes",
        json={"content": "Remember to test the application."},
    )
    assert create_response.status_code == 201
    note = create_response.json()
    assert note["task_id"] == task_id
    assert note["content"] == "Remember to test the application."

    list_response = client.get(f"/api/v1/tasks/{task_id}/notes")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1


def test_update_note():
    task_id = create_test_task()
    create_response = client.post(
        f"/api/v1/tasks/{task_id}/notes",
        json={"content": "Original note"},
    )
    note_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/notes/{note_id}",
        json={"content": "Updated note"},
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated note"


def test_delete_note():
    task_id = create_test_task()
    create_response = client.post(
        f"/api/v1/tasks/{task_id}/notes",
        json={"content": "Note to delete"},
    )
    note_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/notes/{note_id}")
    assert response.status_code == 204
