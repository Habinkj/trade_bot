from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from kiteconnect import KiteConnect
import json
from backend.strategy import generate_signal

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== ZERODHA CONFIG ==================

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

kite = KiteConnect(api_key=API_KEY)

ACCESS_TOKEN = None  # Will store session after login

# ================== BASIC ROUTES ==================

@app.get("/")
def home():
    return {"message": "Trading Bot Backend Running"}

@app.get("/scan")
def scan():
    return scan_market()

@app.post("/predict")
def predict(symbol: str):
    return generate_signal(symbol)

# ================== ZERODHA LOGIN ==================

@app.get("/login")
def login():
    login_url = kite.login_url()
    return {"login_url": login_url}

@app.get("/callback")
def callback(request_token: str):
    global ACCESS_TOKEN

    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        ACCESS_TOKEN = data["access_token"]
        kite.set_access_token(ACCESS_TOKEN)

        return {
            "status": "Login successful",
            "user_id": data["user_id"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ================== SAFE REAL ORDER ==================

@app.post("/order")
def place_order(symbol: str, qty: int, side: str):
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    # 🛑 SAFETY LIMITS
    if qty > 5:
        return JSONResponse(status_code=400, content={"error": "Max qty allowed is 5"})

    if side.lower() not in ["buy", "sell"]:
        return JSONResponse(status_code=400, content={"error": "Side must be BUY or SELL"})

    try:
        kite.set_access_token(ACCESS_TOKEN)

        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol.upper(),
            transaction_type=kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" else kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=kite.PRODUCT_MIS,  # Intraday only
            order_type=kite.ORDER_TYPE_MARKET
        )

        return {
            "status": "Order placed",
            "order_id": order_id,
            "symbol": symbol.upper(),
            "qty": qty,
            "side": side.upper()
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})