from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import router

app = FastAPI()

# Include API routes
app.include_router(router)

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Serve main page
@app.get("/")
def serve_home():
    return FileResponse("frontend/index.html")


# Optional: if you had /login before
@app.get("/login")
def serve_login():
    return FileResponse("frontend/index.html")