from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead


router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
