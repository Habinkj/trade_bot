import pandas as pd
from backend.indicators import calculate_adx
from backend.indicators import calculate_supertrend

# -------- SMA (5,10) --------
def sma_5_10_signal(df):
    df["sma_5"] = df["close"].rolling(5).mean()
    df["sma_10"] = df["close"].rolling(10).mean()

    adx = calculate_adx(df)
    latest_adx = adx.iloc[-1]

    prev_fast = df["sma_5"].iloc[-2]
    prev_slow = df["sma_10"].iloc[-2]
    curr_fast = df["sma_5"].iloc[-1]
    curr_slow = df["sma_10"].iloc[-1]

    bullish_cross = prev_fast <= prev_slow and curr_fast > curr_slow
    bearish_cross = prev_fast >= prev_slow and curr_fast < curr_slow

    strong_trend = latest_adx > 25

    if bullish_cross and strong_trend:
        return "BUY"

    if bearish_cross and strong_trend:
        return "SELL"

    return "HOLD"

# -------- SMA (9,21) --------
def sma_9_21_signal(df):
    df["sma_9"] = df["close"].rolling(9).mean()
    df["sma_21"] = df["close"].rolling(21).mean()

    adx = calculate_adx(df)
    latest_adx = adx.iloc[-1]

    prev_fast = df["sma_9"].iloc[-2]
    prev_slow = df["sma_21"].iloc[-2]
    curr_fast = df["sma_9"].iloc[-1]
    curr_slow = df["sma_21"].iloc[-1]

    bullish_cross = prev_fast <= prev_slow and curr_fast > curr_slow
    bearish_cross = prev_fast >= prev_slow and curr_fast < curr_slow

    strong_trend = latest_adx > 25

    if bullish_cross and strong_trend:
        return "BUY"

    if bearish_cross and strong_trend:
        return "SELL"

    return "HOLD"


# -------- SMA (15,20) --------
def sma_15_20_signal(df):
    df["sma_15"] = df["close"].rolling(15).mean()
    df["sma_20"] = df["close"].rolling(20).mean()

    adx = calculate_adx(df)
    latest_adx = adx.iloc[-1]

    prev_fast = df["sma_15"].iloc[-2]
    prev_slow = df["sma_20"].iloc[-2]
    curr_fast = df["sma_15"].iloc[-1]
    curr_slow = df["sma_20"].iloc[-1]

    bullish_cross = prev_fast <= prev_slow and curr_fast > curr_slow
    bearish_cross = prev_fast >= prev_slow and curr_fast < curr_slow

    strong_trend = latest_adx > 25

    if bullish_cross and strong_trend:
        return "BUY"

    if bearish_cross and strong_trend:
        return "SELL"

    return "HOLD"


# ---------- EMA CROSSOVER ----------
def ema_cross_signal(df):
    df["ema_fast"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=21, adjust=False).mean()
    df["ema_trend"] = df["close"].ewm(span=50, adjust=False).mean()

    adx = calculate_adx(df)
    latest_adx = adx.iloc[-1]

    prev_fast = df["ema_fast"].iloc[-2]
    prev_slow = df["ema_slow"].iloc[-2]

    curr_fast = df["ema_fast"].iloc[-1]
    curr_slow = df["ema_slow"].iloc[-1]
    curr_price = df["close"].iloc[-1]
    curr_trend = df["ema_trend"].iloc[-1]

    bullish_cross = prev_fast <= prev_slow and curr_fast > curr_slow
    trend_ok = curr_price > curr_trend
    strong_trend = latest_adx > 25

    if bullish_cross and trend_ok and strong_trend:
        return "BUY"

    return "HOLD"

# -------- SUPER TREND ----------
def supertrend_signal(df):
    st = calculate_supertrend(df)

    price = df["close"].iloc[-1]

    if price > st.iloc[-1]:
        return "BUY"
    else:
        return "SELL"