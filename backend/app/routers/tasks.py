from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.task import Task, TaskPriority
from app.schemas.task import TaskCreate, TaskRead


router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    completed: bool | None = Query(default=None),
    priority: TaskPriority | None = Query(default=None),
    session: Session = Depends(get_session),
):
    statement = select(Task)
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    return session.exec(statement).all()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
