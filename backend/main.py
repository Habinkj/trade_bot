from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.strategy import generate_signal

app = FastAPI()

# CORS (allows frontend or external apps to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (REQUIRED for Render to know app is alive)
@app.get("/")
def root():
    return {"status": "Trade bot API running"}

# Trading signal route
@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    return generate_signal(symbol)
