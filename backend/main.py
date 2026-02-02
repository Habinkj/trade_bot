from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api import router  # your existing API routes

app = FastAPI()

# Include your API routes
app.include_router(router)

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve dashboard homepage
@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))