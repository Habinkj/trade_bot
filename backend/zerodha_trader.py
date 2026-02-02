from kiteconnect import KiteConnect
import os
import pandas as pd
from datetime import datetime, timedelta

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)

if ACCESS_TOKEN:
    kite.set_access_token(ACCESS_TOKEN)


# ================== DATA FETCH ==================
def get_candles(symbol, interval="5minute", days=5):
    try:
        instrument = f"NSE:{symbol.upper()}"
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)

        data = kite.historical_data(instrument, from_date, to_date, interval)
        return data
    except Exception as e:
        print("Candle fetch error:", e)
        return []


# ================== STRATEGIES ==================
def check_strategy(symbol, strategy):
    candles = get_candles(symbol)

    if len(candles) < 50:
        return None

    df = pd.DataFrame(candles)

    # --- SMA Crossover (9/21) ---
    if strategy == "crossover":
        df["sma_fast"] = df["close"].rolling(9).mean()
        df["sma_slow"] = df["close"].rolling(21).mean()

        if df["sma_fast"].iloc[-2] < df["sma_slow"].iloc[-2] and df["sma_fast"].iloc[-1] > df["sma_slow"].iloc[-1]:
            return f"{symbol} BUY (SMA Cross)"

    # --- Price Above SMA ---
    elif strategy == "price":
        df["sma"] = df["close"].rolling(20).mean()
        if df["close"].iloc[-1] > df["sma"].iloc[-1]:
            return f"{symbol} BUY (Price > SMA)"

    # --- Triple SMA ---
    elif strategy == "triple":
        df["sma_short"] = df["close"].rolling(5).mean()
        df["sma_mid"] = df["close"].rolling(13).mean()
        df["sma_long"] = df["close"].rolling(34).mean()

        if df["sma_short"].iloc[-1] > df["sma_mid"].iloc[-1] > df["sma_long"].iloc[-1]:
            return f"{symbol} BUY (Triple SMA)"

    return None