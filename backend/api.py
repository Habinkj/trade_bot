from fastapi import APIRouter
from backend.data_provider import get_historical
from backend.strategy import sma_signal, ema_signal
from backend.config_loader import load_watchlist
from fastapi.responses import RedirectResponse
from kiteconnect import KiteConnect
import os
from backend.zerodha_session import save_access_token
from backend.strategy import ema_cross_signal
from backend.strategy import (
    sma_fast_signal,
    sma_slow_signal,
    sma_cross_signal,
    ema_cross_signal   # 👈 ADD THIS
)

router = APIRouter()

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

kite = KiteConnect(api_key=API_KEY)  # ✅ this is OK (does NOT need login yet)



@router.get("/scan")
def scan_market(strategy: str = "sma_cross"):
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
                raise ValueError("Invalid strategy")

            if signal == "BUY":
                results.append(symbol)

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results

@router.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


@router.get("/callback")
def callback(request_token: str):
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]
    save_access_token(access_token)
    return RedirectResponse("/")