import pandas as pd
import numpy as np

# ATR (Average True Range)
def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr


# ADX (Average Directional Movement Index)
def calculate_adx(df, period=14):
    df = df.copy()

    df["+DM"] = np.where(
        (df["high"] - df["high"].shift()) > (df["low"].shift() - df["low"]),
        np.maximum(df["high"] - df["high"].shift(), 0),
        0,
    )

    df["-DM"] = np.where(
        (df["low"].shift() - df["low"]) > (df["high"] - df["high"].shift()),
        np.maximum(df["low"].shift() - df["low"], 0),
        0,
    )

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift()).abs()
    tr3 = (df["low"] - df["close"].shift()).abs()

    df["TR"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df["ATR"] = df["TR"].rolling(period).mean()

    df["+DI"] = 100 * (df["+DM"].rolling(period).mean() / df["ATR"])
    df["-DI"] = 100 * (df["-DM"].rolling(period).mean() / df["ATR"])

    df["DX"] = 100 * (abs(df["+DI"] - df["-DI"]) / (df["+DI"] + df["-DI"]))
    adx = df["DX"].rolling(period).mean()

    return adx

def calculate_sma(df, period):
    return df["close"].rolling(period).mean()

def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


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