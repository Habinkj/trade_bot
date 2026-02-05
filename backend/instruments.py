import os
import requests
import csv

INSTRUMENTS_FILE = "backend/data/instruments.csv"


def download_instruments():
    """Download full Zerodha instruments list"""
    url = "https://api.kite.trade/instruments"
    r = requests.get(url)

    os.makedirs("backend/data", exist_ok=True)

    with open(INSTRUMENTS_FILE, "wb") as f:
        f.write(r.content)

    print("Saved instruments file.")


def get_token(symbol: str):
    """Find instrument token for NSE equity symbol"""
    if not os.path.exists(INSTRUMENTS_FILE):
        download_instruments()

    with open(INSTRUMENTS_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if (
                row["tradingsymbol"] == symbol
                and row["exchange"] == "NSE"
                and row["instrument_type"] == "EQ"
            ):
                return row["instrument_token"]

    raise Exception(f"Token not found for {symbol}")