import requests
import pandas as pd
from io import StringIO

INSTRUMENTS_URL = "https://api.kite.trade/instruments"

def load_instruments():
    response = requests.get(INSTRUMENTS_URL)
    df = pd.read_csv(StringIO(response.text))
    return df

def get_token(symbol):
    df = load_instruments()
    row = df[(df["tradingsymbol"] == symbol) & (df["exchange"] == "NSE")]
    if not row.empty:
        return int(row.iloc[0]["instrument_token"])
    return None