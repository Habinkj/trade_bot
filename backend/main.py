import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from kiteconnect import KiteConnect

app = FastAPI()

# Load API credentials from Render environment variables
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)


# ✅ Health check
@app.get("/")
def home():
    return {"message": "Trade bot API is running 🚀"}


# 🔹 Step 1 — Redirect user to Zerodha login
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# 🔹 Step 2 — Zerodha redirects back here with request_token
@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    if not request_token:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing request_token from Zerodha"}
        )

    try:
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        kite.set_access_token(data["access_token"])

        return {
            "status": "Login successful",
            "access_token": data["access_token"],
            "user_id": data["user_id"]
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# 🔹 Step 3 — Get Live Market Price
@app.get("/ltp/{symbol}")
def get_ltp(symbol: str):
    try:
        instrument = f"NSE:{symbol.upper()}"
        data = kite.ltp(instrument)
        price = data[instrument]["last_price"]

        return {
            "symbol": symbol.upper(),
            "last_price": price
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )