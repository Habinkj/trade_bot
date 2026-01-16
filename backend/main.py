from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.strategy import generate_signal

app = FastAPI()

# ✅ ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    return generate_signal(symbol)