from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router, kite
import os
import asyncio
import httpx 

# ==========================================
# 1. INITIALIZE APP
# ==========================================
app = FastAPI(title="TRADEBOT ID: 2162", version="2.0", description="Intelligent Computing Swing Trading Architecture")

# ==========================================
# 2. CORS MIDDLEWARE
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. DIRECTORIES
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

# ==========================================
# 4. AUTONOMOUS HEARTBEAT MONITOR
# ==========================================
async def monitor_lifecycle_heartbeat():
    print("🚀 RISK MONITOR ONLINE: Tracking 2% TSL & Confluence Rules")
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get("http://127.0.0.1:8000/auto-sell")
                if response.status_code == 200:
                    exits = response.json()
                    if isinstance(exits, list):
                        for e in exits:
                            print(f"🚨 SELL EXECUTED: {e.get('symbol', 'UNKNOWN')} | {e.get('reason', 'Auto-Exit')} | PnL: {e.get('pnl', 0.0)}%")
            except httpx.RequestError:
                pass # Server booting
            except Exception as e:
                print(f"⚠️ Heartbeat Exception: {e}")
            
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_lifecycle_heartbeat())

# ==========================================
# 5. ROUTERS & STATIC FILES
# ==========================================
app.include_router(router)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ==========================================
# 6. FRONTEND PAGE ROUTES
# ==========================================
@app.get("/")
def serve_home():
    """Serves the main trading dashboard."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/login")
def serve_login():
    """
    The Official Zerodha Security Gateway.
    Redirects the browser to Kite's actual login page.
    """
    return RedirectResponse(url=kite.login_url())

@app.get("/callback")
def kite_callback(request_token: str):
    """
    Catches the request_token from Zerodha after a successful login,
    exchanges it for the daily access_token, and redirects to the dashboard.
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_secret = os.getenv("KITE_API_SECRET")
    
    if not api_secret:
        return {"error": "FATAL: KITE_API_SECRET is missing from your .env file!"}
        
    try:
        # 1. Exchange the request_token for a live access_token
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        
        # 2. Inject the token into your active Kite instance
        kite.set_access_token(access_token)
        
        # 3. Print it to the terminal so you can save it for later
        print("\n" + "="*50)
        print("✅ ZERODHA AUTHENTICATION SUCCESSFUL")
        print("🚨 COPY THIS TO YOUR .env FILE SO YOU DON'T HAVE TO LOGIN AGAIN TODAY:")
        print(f"KITE_ACCESS_TOKEN={access_token}")
        print("="*50 + "\n")
        
        # 4. Redirect seamlessly back to the main terminal UI
        return RedirectResponse(url="/")
        
    except Exception as e:
        return {"error": f"Zerodha Token Exchange Failed: {str(e)}"}