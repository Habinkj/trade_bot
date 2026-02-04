from backend.data_provider import get_historical

def check_strategy(symbol, strategy):
    df = get_historical(symbol)

    if df is None or len(df) < 50:
        return None, None

    # --- Select SMA settings ---
    if strategy == "sma_fast":
        fast, slow = 5, 9
    elif strategy == "sma_mid":
        fast, slow = 9, 21
    else:  # sma_slow
        fast, slow = 13, 34

    # --- Calculate moving averages ---
    df["fast"] = df["close"].rolling(fast).mean()
    df["slow"] = df["close"].rolling(slow).mean()

    # --- TEST LOGIC (trend only, not crossover) ---
    if df["fast"].iloc[-1] > df["slow"].iloc[-1]:
        return "BUY", float(df["close"].iloc[-1])

    return None, float(df["close"].iloc[-1])