import json
from backend.indicators import calculate_sma, calculate_adx
from backend.data_provider import fetch_intraday_data

def load_watchlist():
    with open("config/watchlist.json") as f:
        return json.load(f)

def generate_signal(symbol: str, mode: str):
    df = fetch_intraday_data(symbol)

    if mode == "FAST":
        short, long = 2, 9
    elif mode == "TREND":
        short, long = 10, 50
    else:
        short, long = 5, 20

    df["SMA_SHORT"] = calculate_sma(df, short)
    df["SMA_LONG"] = calculate_sma(df, long)
    df["ADX"] = calculate_adx(df)

    latest = df.iloc[-1]

    if latest["SMA_SHORT"] > latest["SMA_LONG"] and latest["ADX"] > 20:
        signal = "BUY"
        reason = "Uptrend with strength"
        confidence = min(95, int(latest["ADX"] + 50))
    elif latest["SMA_SHORT"] < latest["SMA_LONG"] and latest["ADX"] > 20:
        signal = "SELL"
        reason = "Downtrend with strength"
        confidence = min(95, int(latest["ADX"] + 50))
    else:
        signal = "HOLD"
        reason = "No strong trend"
        confidence = 50

    return {
        "symbol": symbol,
        "signal": signal,
        "reason": reason,
        "confidence": confidence
    }

def scan_market():
    watchlist = load_watchlist()
    results = []
    for stock in watchlist:
        res = generate_signal(stock, "DEFAULT")
        if res["signal"] != "HOLD":
            results.append(res)
    return results