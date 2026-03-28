from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import router
import os

app = FastAPI()

# -------------------------------
# PATH FIX (CRITICAL)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ../frontend relative to backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

# -------------------------------
# ROUTES
# -------------------------------
app.include_router(router)

# -------------------------------
# STATIC FILES (FIXED)
# -------------------------------
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# -------------------------------
# SERVE FRONTEND
# -------------------------------
@app.get("/")
def serve_home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/login")
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))