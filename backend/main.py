from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import router
import os

app = FastAPI()

# Include API routes
app.include_router(router)

# Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Serve the frontend dashboard at "/"
@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")