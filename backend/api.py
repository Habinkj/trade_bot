from fastapi import APIRouter
from backend.data_provider import get_historical
from backend.strategy import (
    sma_fast_signal,
    sma_slow_signal,
    sma_cross_signal,
    ema_cross_signal
)
import json

router = APIRouter()


# ---------- LOAD WATCHLIST ----------
def load_watchlist():
    with open("config/watchlist.json") as f:
        return json.load(f)


# ---------- MARKET SCAN ----------
@router.get("/scan")
def scan_market(strategy: str):
    symbols = load_watchlist()
    results = []

    for symbol in symbols:
        try:
            df = get_historical(symbol)

            if df is None or len(df) < 30:
                continue

            # Choose strategy
            if strategy == "sma_fast":
                signal = sma_fast_signal(df)

            elif strategy == "sma_slow":
                signal = sma_slow_signal(df)

            elif strategy == "sma_cross":
                signal = sma_cross_signal(df)

            elif strategy == "ema_cross":
                signal = ema_cross_signal(df)

            else:
                signal = "HOLD"

            if signal == "BUY":
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal
                })

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results