from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.note import Note
from app.models.task import Task, TaskPriority
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


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


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    notes = session.exec(select(Note).where(Note.task_id == task_id)).all()
    for note in notes:
        session.delete(note)

    session.delete(task)
    session.commit()
    return None


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
