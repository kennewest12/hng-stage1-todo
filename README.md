# HNG Stage 1 To-Do List

An AI-built To-Do List application created for HNG Internship 15 Stage 1.

## Planned Features

- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Mark tasks as completed
- Add and manage notes
- Set task priority
- Filter tasks

## Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS

### Backend
- FastAPI
- Pydantic
- SQLModel
- PostgreSQL

### Testing
- Pytest
- FastAPI TestClient

## Project Structure

```text
hng-stage1-todo/
├── frontend/
├── backend/
├── AGENTS.md
├── README.md
└── .gitignore
```

## Environment Variables

### Backend

Create `backend/.env` locally from `backend/.env.example` and set your PostgreSQL connection string.

### Frontend

The frontend uses `VITE_API_URL` to locate the backend API. If it is not set, it defaults to `http://localhost:8000`.

Example:

```text
VITE_API_URL=http://localhost:8000
```

## Development

The project is being built incrementally. Each feature should be implemented, tested locally, and validated before moving to the next feature.

## Status

Stage 1 development in progress.
