from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import your API router
from backend.api import router

app = FastAPI()

# Include API routes
app.include_router(router)

# -----------------------------
# PATH SETUP (FIXED FOR RENDER)
# -----------------------------

# Folder where this file lives → /backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level UP → project root
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Frontend folder path → /frontend
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# -----------------------------
# SERVE STATIC FILES (CSS & JS)
# -----------------------------

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -----------------------------
# SERVE DASHBOARD (INDEX.HTML)
# -----------------------------

@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))