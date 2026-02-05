def calculate_sma(df, period):
    return df["close"].rolling(period).mean()

def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()

import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def ema_crossover(df, fast=9, slow=21):
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)

    # Previous candle
    prev_fast = df["ema_fast"].iloc[-2]
    prev_slow = df["ema_slow"].iloc[-2]

    # Current candle
    curr_fast = df["ema_fast"].iloc[-1]
    curr_slow = df["ema_slow"].iloc[-1]

    # BUY signal → Fast EMA crosses above Slow EMA
    if prev_fast < prev_slow and curr_fast > curr_slow:
        return "BUY"

    # SELL signal → Fast EMA crosses below Slow EMA
    if prev_fast > prev_slow and curr_fast < curr_slow:
        return "SELL"

    return "HOLD"


def ema_fast_signal(df):
    df["ema5"] = ema(df["close"], 5)
    df["ema13"] = ema(df["close"], 13)

    if df["ema5"].iloc[-1] > df["ema13"].iloc[-1]:
        return "BUY"
    elif df["ema5"].iloc[-1] < df["ema13"].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"