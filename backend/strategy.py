import pandas as pd


# ---------- SMA FAST ----------
def sma_fast_signal(df):
    df["sma_fast"] = df["close"].rolling(5).mean()
    return "BUY" if df["close"].iloc[-1] > df["sma_fast"].iloc[-1] else "HOLD"


# ---------- SMA SLOW ----------
def sma_slow_signal(df):
    df["sma_slow"] = df["close"].rolling(20).mean()
    return "BUY" if df["close"].iloc[-1] > df["sma_slow"].iloc[-1] else "HOLD"


# ---------- SMA CROSSOVER ----------
def sma_cross_signal(df):
    df["sma_fast"] = df["close"].rolling(9).mean()
    df["sma_slow"] = df["close"].rolling(21).mean()

    if df["sma_fast"].iloc[-2] < df["sma_slow"].iloc[-2] and df["sma_fast"].iloc[-1] > df["sma_slow"].iloc[-1]:
        return "BUY"

    return "HOLD"


# ---------- EMA CROSSOVER ----------
def ema_cross_signal(df):
    df["ema_fast"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=21, adjust=False).mean()
    df["ema_trend"] = df["close"].ewm(span=50, adjust=False).mean()  # Trend filter

    # Previous candle
    prev_fast = df["ema_fast"].iloc[-2]
    prev_slow = df["ema_slow"].iloc[-2]

    # Current candle
    curr_fast = df["ema_fast"].iloc[-1]
    curr_slow = df["ema_slow"].iloc[-1]
    curr_price = df["close"].iloc[-1]
    curr_trend = df["ema_trend"].iloc[-1]

    # Conditions
    bullish_cross = prev_fast <= prev_slow and curr_fast > curr_slow
    trend_ok = curr_price > curr_trend  # Only buy in uptrend

    if bullish_cross and trend_ok:
        return "BUY"

    return "HOLD"