from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os

from backend.zerodha_session import get_kite, get_login_url, save_access_token
from backend.data_provider import get_historical
from backend.strategy import (
    sma_fast_signal,
    sma_slow_signal,
    sma_cross_signal,
    ema_cross_signal
)
from backend.config_loader import load_watchlist

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

router = APIRouter()

# 👉 Step 1 — Redirect user to Zerodha login
@router.get("/login")
def login():
    login_url = get_login_url()
    return RedirectResponse(login_url)

# 👉 Step 2 — Zerodha sends user back here after login
@router.get("/callback")
def callback(request_token: str):
    kite = KiteConnect(api_key=API_KEY)
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]

    save_access_token(access_token)

    return {"status": "Login successful. You can close this tab."}

# 👉 Step 3 — Scan watchlist based on selected strategy
@router.get("/scan")
def scan(strategy: str):
    try:
        kite = get_kite()
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"login_url": get_login_url()}
        )

    watchlist = load_watchlist()
    results = []

    for symbol in watchlist:
        try:
            df = get_historical(symbol)

            if strategy == "sma_fast":
                signal = sma_fast_signal(df)
            elif strategy == "sma_slow":
                signal = sma_slow_signal(df)
            elif strategy == "sma_cross":
                signal = sma_cross_signal(df)
            elif strategy == "ema_cross":
                signal = ema_cross_signal(df)
            else:
                continue

            if signal == "BUY":
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal
                })

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results

