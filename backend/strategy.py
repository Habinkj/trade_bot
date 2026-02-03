import pandas as pd

def sma_signal(candles, fast, slow):
    df = pd.DataFrame(candles)

    df["sma_fast"] = df["close"].rolling(fast).mean()
    df["sma_slow"] = df["close"].rolling(slow).mean()

    if df["sma_fast"].iloc[-1] > df["sma_slow"].iloc[-1]:
        return "BUY"
    return None