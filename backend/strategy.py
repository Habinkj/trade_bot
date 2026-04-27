import pandas as pd
from backend.indicators import calculate_supertrend

def sma_dynamic_signal(df, fast_period, slow_period):
    """
    Calculates SMA crossover using user-defined periods.
    """
    df["sma_fast"] = df["close"].rolling(fast_period).mean()
    df["sma_slow"] = df["close"].rolling(slow_period).mean()
    
    if len(df) < slow_period: return "WAIT"
    
    curr_fast, prev_fast = df["sma_fast"].iloc[-1], df["sma_fast"].iloc[-2]
    curr_slow, prev_slow = df["sma_slow"].iloc[-1], df["sma_slow"].iloc[-2]
    
    # Logic for exact crossover point
    if prev_fast <= prev_slow and curr_fast > curr_slow:
        return "BUY"
    elif prev_fast >= prev_slow and curr_fast < curr_slow:
        return "SELL"
    
    # Shows the current relative position for the demo
    current_trend = "Up" if curr_fast > curr_slow else "Down"
    return f"HOLD ({current_trend})"

def ema_cross_signal(df, fast_period, slow_period):
    """
    Calculates EMA crossover using user-defined periods.
    """
    df["ema_fast"] = df["close"].ewm(span=fast_period, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=slow_period, adjust=False).mean()
    
    if len(df) < slow_period: return "WAIT"
    
    curr_f, prev_f = df["ema_fast"].iloc[-1], df["ema_fast"].iloc[-2]
    curr_s, prev_s = df["ema_slow"].iloc[-1], df["ema_slow"].iloc[-2]
    
    if prev_f <= prev_s and curr_f > curr_s:
        return "BUY"
    elif prev_f >= prev_s and curr_f < curr_s:
        return "SELL"
    
    current_trend = "Up" if curr_f > curr_s else "Down"
    return f"HOLD ({current_trend})"

def supertrend_signal(df, period, multiplier):
    """
    FIXED: Uses 'ST_Trend' keyword and shows active trend state.
    """
    # st_df now contains the 'ST_Trend' column created in indicators.py
    st_df = calculate_supertrend(df, period=period, multiplier=multiplier)
    
    curr_st = st_df["ST_Trend"].iloc[-1]
    prev_st = st_df["ST_Trend"].iloc[-2]
    
    # 1. Check for the 'FLIP' (The best entry point)
    if prev_st == "Down" and curr_st == "Up":
        return "BUY"
    elif prev_st == "Up" and curr_st == "Down":
        return "SELL"
    
    # 2. If no flip, show the CURRENT trend direction
    # This ensures your dashboard looks "Alive" during the project demo.
    return f"HOLD ({curr_st})"