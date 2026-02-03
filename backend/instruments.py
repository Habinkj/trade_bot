import requests
import pandas as pd
from io import StringIO

# ✅ YOUR MASTER WATCHLIST
WATCHLIST = [
    "RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","ITC","LT",
    "AXISBANK","KOTAKBANK","HINDUNILVR","BAJFINANCE","MARUTI",
    "ASIANPAINT","SUNPHARMA","TITAN","ULTRACEMCO","WIPRO","NTPC",
    "POWERGRID","TATAMOTORS","ADANIPORTS","JSWSTEEL","ONGC"
]

INSTRUMENTS_URL = "https://api.kite.trade/instruments"

INSTRUMENTS_DF = None


def load_instruments():
    global INSTRUMENTS_DF

    if INSTRUMENTS_DF is None:
        print("📥 Downloading instruments list once...")
        response = requests.get(INSTRUMENTS_URL)
        INSTRUMENTS_DF = pd.read_csv(StringIO(response.text))

    return INSTRUMENTS_DF


def get_token(symbol: str):
    df = load_instruments()
    row = df[(df["tradingsymbol"] == symbol) & (df["exchange"] == "NSE")]

    if not row.empty:
        return int(row.iloc[0]["instrument_token"])

    return None