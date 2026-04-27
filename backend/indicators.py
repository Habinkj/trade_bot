import pandas as pd
import numpy as np

# --------------------------------------------------
# ATR (Average True Range) - Wilder's Smoothing
# --------------------------------------------------
def calculate_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift(1)).abs()
    low_close = (df["low"] - df["close"].shift(1)).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/period, adjust=False).mean()
    return atr

# --------------------------------------------------
# ADX (Average Directional Index) - Precise Version
# --------------------------------------------------
def calculate_adx(df, period=14):
    df = df.copy()
    alpha = 1 / period
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift(1)).abs()
    tr3 = (df["low"] - df["close"].shift(1)).abs()
    df["TR"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df["up_move"] = df["high"] - df["high"].shift(1)
    df["down_move"] = df["low"].shift(1) - df["low"]
    df["+DM"] = np.where((df["up_move"] > df["down_move"]) & (df["up_move"] > 0), df["up_move"], 0.0)
    df["-DM"] = np.where((df["down_move"] > df["up_move"]) & (df["down_move"] > 0), df["down_move"], 0.0)
    smooth_tr = df["TR"].ewm(alpha=alpha, adjust=False).mean()
    smooth_plus_dm = df["+DM"].ewm(alpha=alpha, adjust=False).mean()
    smooth_minus_dm = df["-DM"].ewm(alpha=alpha, adjust=False).mean()
    df["+DI"] = 100 * (smooth_plus_dm / smooth_tr)
    df["-DI"] = 100 * (smooth_minus_dm / smooth_tr)
    df["DX"] = 100 * (abs(df["+DI"] - df["-DI"]) / (df["+DI"] + df["-DI"]))
    adx = df["DX"].ewm(alpha=alpha, adjust=False).mean()
    return adx

# --------------------------------------------------
# BASIC INDICATORS (SMA, EMA, SUPERTREND)
# --------------------------------------------------
def calculate_sma(df, period):
    return df["close"].rolling(period).mean()

def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()

def calculate_supertrend(df, period=10, multiplier=3):
    """
    Calculates Supertrend and creates the ST_Trend keyword.
    """
    df = df.copy()
    atr = calculate_atr(df, period)
    hl2 = (df["high"] + df["low"]) / 2
    
    df["upperband"] = hl2 + (multiplier * atr)
    df["lowerband"] = hl2 - (multiplier * atr)
    df["in_uptrend"] = True

    for i in range(1, len(df)):
        if df["close"].iloc[i] > df["upperband"].iloc[i-1]:
            df.loc[df.index[i], "in_uptrend"] = True
        elif df["close"].iloc[i] < df["lowerband"].iloc[i-1]:
            df.loc[df.index[i], "in_uptrend"] = False
        else:
            df.loc[df.index[i], "in_uptrend"] = df.iloc[i-1]["in_uptrend"]

    # This creates the keyword 'ST_Trend' that your strategy expects
    df["ST_Trend"] = np.where(df["in_uptrend"], "Up", "Down")
    return df