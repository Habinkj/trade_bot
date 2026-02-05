def calculate_sma(df, period):
    return df["close"].rolling(period).mean()

def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()