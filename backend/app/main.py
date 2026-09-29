from fastapi import FastAPI

from app.routers.notes import router as notes_router
from app.routers.tasks import router as tasks_router


app = FastAPI(title="HNG Stage 1 To-Do API", version="1.0.0")

app.include_router(tasks_router)
app.include_router(notes_router)


@app.get("/health")
def health_check():
    return {"success": True, "message": "API is running"}
