# backend/strategy.py
from backend.data_provider import get_candles

def generate_signal(symbol: str):
    df = get_candles(symbol)

    # SIMPLE SMA STRATEGY (baseline, not holy grail)
    df["sma_fast"] = df["close"].rolling(5).mean()
    df["sma_slow"] = df["close"].rolling(20).mean()

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    if prev["sma_fast"] < prev["sma_slow"] and latest["sma_fast"] > latest["sma_slow"]:
        return {"signal": "BUY"}

    if prev["sma_fast"] > prev["sma_slow"] and latest["sma_fast"] < latest["sma_slow"]:
        return {"signal": "SELL"}

    return {"signal": "HOLD"}
