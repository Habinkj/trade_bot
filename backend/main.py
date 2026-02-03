from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from kiteconnect import KiteConnect
import os

from backend.data_provider import get_ltp, get_historical
from backend.strategy import sma_signal
from backend.instruments import WATCHLIST


app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ===== CONFIG (from Render Environment) =====
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

if not API_KEY or not API_SECRET:
    print("⚠ Zerodha API keys not set in environment variables")

kite = KiteConnect(api_key=API_KEY) if API_KEY else None

# Temporary session storage (resets when server restarts)
ACCESS_TOKEN = None


# ==================================================
# 🔐 STEP 1 – Send user to Zerodha Login
# ==================================================
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# ==================================================
# 🔐 STEP 2 – Zerodha redirects back here
# ==================================================
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

        return RedirectResponse("/")  # back to dashboard

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ==================================================
# 📈 MARKET SCAN
# ==================================================
@app.get("/scan")
def scan_market(strategy: str):
    if ACCESS_TOKEN is None:
        return JSONResponse(status_code=401, content={"error": "Login required"})

    results = []

    for symbol in WATCHLIST:
        try:
            candles = get_historical(symbol, interval="5minute", days=5)
            signal = sma_signal(candles, strategy)

            if signal == "BUY":
                ltp = get_ltp(symbol)
                results.append({
                    "symbol": symbol,
                    "price": round(ltp, 2),
                    "signal": "BUY"
                })

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results


# ==================================================
# 🛒 PLACE ORDER (BUY ONLY)
# ==================================================
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


# ==================================================
# 💰 BALANCE CHECK
# ==================================================
@app.get("/balance")
def get_balance():
    global ACCESS_TOKEN

    if not ACCESS_TOKEN:
        return {"balance": 0}

    try:
        kite.set_access_token(ACCESS_TOKEN)
        margins = kite.margins("equity")
        cash = margins["available"]["cash"]

        return {"balance": round(cash, 2)}

    except Exception as e:
        return {"balance": 0, "error": str(e)}


# ==================================================
# 🖥 FRONTEND ROUTES
# ==================================================
@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")


@app.get("/home")
def home():
    return FileResponse("frontend/index.html")