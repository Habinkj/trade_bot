import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from kiteconnect import KiteConnect

app = FastAPI()

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

# ===== GLOBAL STATE =====
ACCESS_TOKEN = None

# ===== RISK CONTROLS =====
MAX_QTY_PER_ORDER = 5
DAILY_LOSS_LIMIT = -1000  # Stop trading if loss exceeds ₹1000


@app.get("/")
def home():
    return {"message": "Trade bot API is running 🚀"}


# ================= LOGIN FLOW =================

@app.get("/login")
def login():
    login_url = kite.login_url()
    return {"login_url": login_url}


@app.get("/callback")
def callback(request: Request):
    global ACCESS_TOKEN

    request_token = request.query_params.get("request_token")

    if not request_token:
        return JSONResponse(status_code=400, content={"error": "Missing request_token"})

    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        ACCESS_TOKEN = data["access_token"]
        kite.set_access_token(ACCESS_TOKEN)

        return {
            "status": "Login successful",
            "access_token": ACCESS_TOKEN,
            "user_id": data["user_id"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ================= ACCOUNT INFO =================

@app.get("/balance")
def get_balance():
    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    try:
        kite.set_access_token(ACCESS_TOKEN)
        margins = kite.margins()

        return {
            "available_cash": margins["equity"]["available"]["cash"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/risk-status")
def risk_status():
    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    try:
        kite.set_access_token(ACCESS_TOKEN)
        positions = kite.positions()
        day_positions = positions.get("day", [])

        total_pnl = sum(p.get("pnl", 0) for p in day_positions)

        if total_pnl <= DAILY_LOSS_LIMIT:
            return {
                "trading_allowed": False,
                "reason": "Daily loss limit hit",
                "pnl": total_pnl
            }

        return {
            "trading_allowed": True,
            "pnl": total_pnl
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ================= SAFE ORDER PLACEMENT =================

@app.post("/order")
def place_order(symbol: str, qty: int, side: str):
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    # 🛑 Quantity Safety Limit
    if qty > MAX_QTY_PER_ORDER:
        return JSONResponse(status_code=400, content={"error": f"Max qty allowed is {MAX_QTY_PER_ORDER}"})

    # 🛑 Side Validation
    if side.lower() not in ["buy", "sell"]:
        return JSONResponse(status_code=400, content={"error": "Side must be BUY or SELL"})

    # 🛑 Daily Loss Check
    risk = risk_status()
    if isinstance(risk, dict) and risk.get("trading_allowed") is False:
        return JSONResponse(status_code=403, content=risk)

    try:
        kite.set_access_token(ACCESS_TOKEN)

        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol.upper(),
            transaction_type=kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" else kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=kite.PRODUCT_MIS,  # Intraday only (safer)
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