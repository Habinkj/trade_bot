from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from kiteconnect import KiteConnect
import os

app = FastAPI()

# Serve CSS + JS
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ====== CONFIG (from Render Environment) ======
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

if not API_KEY or not API_SECRET:
    print("⚠️ Zerodha API keys not set yet. Add them in Render environment variables.")

kite = KiteConnect(api_key=API_KEY) if API_KEY else None

# This stores login session TEMPORARILY (resets if server restarts — that’s OK)
ACCESS_TOKEN = None


# ============================================
# 🔐 STEP 1 — Send user to Zerodha Login
# ============================================
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# ============================================
# 🔐 STEP 2 — Zerodha redirects back here
# ============================================
@app.get("/callback")
def callback(request: Request):
    global ACCESS_TOKEN

    request_token = request.query_params.get("request_token")

    if not request_token:
        return JSONResponse(status_code=400, content={"error": "Request token missing"})

    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        ACCESS_TOKEN = data["access_token"]
        kite.set_access_token(ACCESS_TOKEN)

        return RedirectResponse("/")  # go back to dashboard after login

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ============================================
# 📊 MARKET SCAN (Dummy SMA scan for UI)
# ============================================
@app.get("/scan")
def scan_market():
    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    # Example mock response — replace with real strategy later
    return [
        {"symbol": "RELIANCE", "price": 2450, "signal": "BUY"},
        {"symbol": "INFY", "price": 1580, "signal": "BUY"},
        {"symbol": "TCS", "price": 4020, "signal": "BUY"},
    ]


# ============================================
# 💰 SAFE REAL ORDER (BUY ONLY)
# ============================================
@app.post("/order")
def place_order(symbol: str, qty: int):
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    if qty > 5:
        return JSONResponse(status_code=400, content={"error": "Max qty allowed is 5"})

    try:
        kite.set_access_token(ACCESS_TOKEN)

        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol.upper(),
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=qty,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )

        return {"status": "Order placed", "order_id": order_id}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

    @app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")