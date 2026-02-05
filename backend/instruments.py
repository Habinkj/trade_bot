import os
import json
import requests

INSTRUMENTS_FILE = "backend/data/instruments.json"
INSTRUMENTS_URL = "https://api.kite.trade/instruments"

def download_instruments():
    """Download full instruments dump from Zerodha and save locally"""
    print("Downloading instruments list...")
    
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {os.getenv('ZERODHA_API_KEY')}:{os.getenv('ZERODHA_ACCESS_TOKEN')}"
    }

    response = requests.get(INSTRUMENTS_URL, headers=headers)
    response.raise_for_status()

    instruments = []
    for line in response.text.split("\n")[1:]:
        if line.strip():
            parts = line.split(",")
            instruments.append({
                "instrument_token": parts[0],
                "exchange": parts[11],
                "tradingsymbol": parts[2],
                "instrument_type": parts[9]
            })

    os.makedirs("backend/data", exist_ok=True)
    with open(INSTRUMENTS_FILE, "w") as f:
        json.dump(instruments, f)

    print(f"Saved {len(instruments)} instruments.")


def load_instruments():
    """Load instruments from local file, download if missing"""
    if not os.path.exists(INSTRUMENTS_FILE):
        download_instruments()

    with open(INSTRUMENTS_FILE, "r") as f:
        return json.load(f)


def get_token(symbol: str):
    """
    Return instrument token for NSE equity symbol
    Example: 'TATAMOTORS' → 884737
    """
    instruments = load_instruments()

    for inst in instruments:
        if (
            inst["exchange"] == "NSE" and
            inst["instrument_type"] == "EQ" and
            inst["tradingsymbol"] == symbol.upper()
        ):
            return int(inst["instrument_token"])

    raise Exception(f"Token not found for {symbol}")