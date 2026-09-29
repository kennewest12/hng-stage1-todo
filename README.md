# HNG Stage 1 To-Do List

An AI-built To-Do List application created for HNG Internship 15 Stage 1.

## Features

- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Mark tasks as completed
- Add, view, update, and delete notes
- Set task priority: low, medium, or high
- Filter tasks by completion status and priority

## Tech Stack

### Frontend
- React
- Vite
- Plain CSS

### Backend
- FastAPI
- Pydantic
- SQLModel
- PostgreSQL

### Testing
- Pytest
- FastAPI TestClient

## Live Application

- Frontend: https://hng-stage1-todo-frontend.onrender.com
- Backend API: https://hng-stage1-todo.onrender.com
- API documentation: https://hng-stage1-todo.onrender.com/docs
- Health check: https://hng-stage1-todo.onrender.com/health

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

The project is built incrementally. Each feature should be implemented, tested locally, and validated before moving to the next feature.

### Run the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

## Status

Stage 1 application deployed on Render with the required To-Do features, notes, priority filtering, automated API tests, and `AGENTS.md` instructions.
