from backend.indicators import calculate_sma, calculate_ema

def sma_signal(df, fast=5, slow=9):
    df["fast"] = calculate_sma(df, fast)
    df["slow"] = calculate_sma(df, slow)

    if df["fast"].iloc[-1] > df["slow"].iloc[-1] and df["fast"].iloc[-2] <= df["slow"].iloc[-2]:
        return "BUY"
    return None

def ema_signal(df, fast=9, slow=21):
    df["fast"] = calculate_ema(df, fast)
    df["slow"] = calculate_ema(df, slow)

    if df["fast"].iloc[-1] > df["slow"].iloc[-1] and df["fast"].iloc[-2] <= df["slow"].iloc[-2]:
        return "BUY"
    return None