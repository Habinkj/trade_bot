from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import router
import os
import asyncio
import httpx # Required: pip install httpx

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

async def monitor_lifecycle_heartbeat():
    """
    Heartbeat Monitor: Triggers Risk Management Every 2 Seconds.
    Ensures 2% SL and 4% Target are monitored autonomously.
    """
    print("🚀 RISK MONITOR ONLINE: Tracking 2% SL | 4% Target")
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                # Internal call to the auto-sell endpoint
                response = await client.get("http://127.0.0.1:8000/auto-sell")
                if response.status_code == 200:
                    exits = response.json()
                    for e in exits:
                        print(f"🚨 SELL EXECUTED: {e['symbol']} | {e['reason']} | PnL: {e['pnl']}%")
            except Exception as e:
                print(f"⚠️ Heartbeat Error: {e}")
            
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    # Launches the background monitor
    asyncio.create_task(monitor_lifecycle_heartbeat())

app.include_router(router)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/login")
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))