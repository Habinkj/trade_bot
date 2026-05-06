import pandas as pd
from backend.indicators import calculate_supertrend, calculate_adx, calculate_rsi

def dual_path_signal(df, st_p=10, st_m=3.0, ema_f=9, ema_s=21, adx_min=25.0, rsi_bounce=40.0):
    """
    Strict Confluence Framework: ALL conditions must be met to trigger a BUY.
    No more loopholes or bypass paths.
    """
    if len(df) < max(ema_s, st_p, 14) + 2:
        return "HOLD", 0.0

    # 1. Generate Indicators
    df["ema_fast"] = df["close"].ewm(span=ema_f, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=ema_s, adjust=False).mean()
    
    adx_series = calculate_adx(df, period=14) 
    st_series = calculate_supertrend(df, period=st_p, multiplier=st_m)
    rsi_series = calculate_rsi(df, period=14)

    curr_close = df["close"].iloc[-1]
    curr_ema_fast = df["ema_fast"].iloc[-1]
    curr_ema_slow = df["ema_slow"].iloc[-1]
    curr_adx = adx_series.iloc[-1]
    curr_rsi = rsi_series.iloc[-1]
    curr_st = st_series.iloc[-1]

    # ==========================================
    # 🛡️ STRICT CONFLUENCE BUY LOGIC
    # ==========================================
    
    # Condition 1: Supertrend must be GREEN (Price > Supertrend)
    supertrend_green = curr_close > curr_st 
    
    # Condition 2: EMA must be Bullish (Fast > Slow)
    ema_bullish = curr_ema_fast > curr_ema_slow
    
    # Condition 3: ADX must show strong trend
    adx_strong = curr_adx >= adx_min
    
    # Condition 4: RSI must show momentum
    rsi_strong = curr_rsi >= rsi_bounce

    # ALL 4 gates must open to trigger the BUY
    if supertrend_green and ema_bullish and adx_strong and rsi_strong:
        return "BUY", curr_adx

    # ==========================================
    # 🚨 SELL LOGIC (Risk Exit)
    # ==========================================
    
    # Immediate exit if the floor drops out
    if curr_close < curr_st:
        return "SELL", curr_adx

    return "HOLD", curr_adx