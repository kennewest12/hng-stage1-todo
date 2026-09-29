from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.models.note import Note
from app.models.task import Task


engine = create_engine(settings.sqlalchemy_database_url, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
