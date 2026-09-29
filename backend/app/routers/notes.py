from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.note import Note
from app.models.task import Task
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate


router = APIRouter(prefix="/api/v1", tags=["Notes"])


@router.post("/tasks/{task_id}/notes", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(task_id: int, note_data: NoteCreate, session: Session = Depends(get_session)):
    if session.get(Task, task_id) is None:
        raise HTTPException(status_code=404, detail="Task not found")

    note = Note(task_id=task_id, content=note_data.content)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.get("/tasks/{task_id}/notes", response_model=list[NoteRead])
def list_notes(task_id: int, session: Session = Depends(get_session)):
    if session.get(Task, task_id) is None:
        raise HTTPException(status_code=404, detail="Task not found")

    statement = select(Note).where(Note.task_id == task_id)
    return session.exec(statement).all()


@router.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note_data: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.content = note_data.content
    note.updated_at = datetime.now(timezone.utc)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()
    return None
