from fastapi import FastAPI
from fastapi.responses import JSONResponse
from kiteconnect import KiteConnect
import os

app = FastAPI()

# 🔐 API credentials from Render Environment Variables
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

# Will store logged-in session token
ACCESS_TOKEN = None


# ------------------ LOGIN ------------------

@app.get("/login")
def login():
    login_url = kite.login_url()
    return {"login_url": login_url}


# ------------------ CALLBACK ------------------

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
        return JSONResponse(status_code=400, content={"error": str(e)})


# ------------------ BALANCE ------------------

@app.get("/balance")
def get_balance():
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    try:
        kite.set_access_token(ACCESS_TOKEN)
        margins = kite.margins()
        available_cash = margins["equity"]["available"]["cash"]

        return {"available_cash": available_cash}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ------------------ RISK STATUS ------------------

@app.get("/risk-status")
def risk_status():
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    try:
        kite.set_access_token(ACCESS_TOKEN)
        positions = kite.positions()

        total_pnl = 0
        for p in positions["day"]:
            total_pnl += p["pnl"]

        trading_allowed = total_pnl > -2000  # Stop trading if loss > ₹2000

        return {
            "trading_allowed": trading_allowed,
            "pnl": total_pnl
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ------------------ SAFE ORDER ------------------

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


# ------------------ POSITIONS ------------------

@app.get("/positions")
def get_positions():
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    try:
        kite.set_access_token(ACCESS_TOKEN)
        positions = kite.positions()

        return {
            "day_positions": positions["day"],
            "net_positions": positions["net"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})