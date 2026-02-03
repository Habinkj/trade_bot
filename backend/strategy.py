from backend.data_provider import get_historical
import pandas as pd


def check_strategy(symbol, strategy):
    df = get_historical(symbol)

    if df is None or len(df) < 50:
        return None, None

    if strategy == "sma_fast":
        fast, slow = 5, 9
    elif strategy == "sma_mid":
        fast, slow = 9, 21
    else:
        fast, slow = 13, 34

    df["fast"] = df["close"].rolling(fast).mean()
    df["slow"] = df["close"].rolling(slow).mean()

    if df["fast"].iloc[-1] > df["slow"].iloc[-1]:
    return "BUY", df["close"].iloc[-1]

    return None, df["close"].iloc[-1]