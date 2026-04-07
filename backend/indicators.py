import pandas as pd
import numpy as np

# ATR (Average True Range) using Wilder's Smoothing to match TradingView
def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    # Wilder's smoothing uses alpha = 1/period
    atr = tr.ewm(alpha=1/period, adjust=False).mean()

    return atr


# ADX (Average Directional Movement Index) - TradingView Compatible Version
def calculate_adx(df, period=14):
    df = df.copy()
    alpha = 1 / period

    # 1. True Range
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift(1)).abs()
    tr3 = (df["low"] - df["close"].shift(1)).abs()
    df["TR"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # 2. Directional Movement
    df["up_move"] = df["high"] - df["high"].shift(1)
    df["down_move"] = df["low"].shift(1) - df["low"]

    df["+DM"] = np.where((df["up_move"] > df["down_move"]) & (df["up_move"] > 0), df["up_move"], 0.0)
    df["-DM"] = np.where((df["down_move"] > df["up_move"]) & (df["down_move"] > 0), df["down_move"], 0.0)

    # 3. Smoothed TR and DM using Wilder's
    smooth_tr = df["TR"].ewm(alpha=alpha, adjust=False).mean()
    smooth_plus_dm = df["+DM"].ewm(alpha=alpha, adjust=False).mean()
    smooth_minus_dm = df["-DM"].ewm(alpha=alpha, adjust=False).mean()

    # 4. DI Indicators
    df["+DI"] = 100 * (smooth_plus_dm / smooth_tr)
    df["-DI"] = 100 * (smooth_minus_dm / smooth_tr)

    # 5. ADX Calculation
    df["DX"] = 100 * (abs(df["+DI"] - df["-DI"]) / (df["+DI"] + df["-DI"]))
    adx = df["DX"].ewm(alpha=alpha, adjust=False).mean()

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

    # Check for sufficient data
    if len(df) < 2:
        return "HOLD"

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
    
def calculate_supertrend(df, period=10, multiplier=3):
    """
    Improved Supertrend logic (Standard version)
    """
    df = df.copy()
    hl2 = (df["high"] + df["low"]) / 2
    atr = calculate_atr(df, period)

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    
    # Returning the lowerband as requested for your current strategy
    return lowerband