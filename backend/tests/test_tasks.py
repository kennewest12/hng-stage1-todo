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
