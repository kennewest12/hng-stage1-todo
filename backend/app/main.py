from fastapi import FastAPI

app = FastAPI(title="HNG Stage 1 To-Do API", version="1.0.0")


@app.get("/health")
def health_check():
    return {"success": True, "message": "API is running"}
