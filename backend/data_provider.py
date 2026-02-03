from kiteconnect import KiteConnect
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)


def get_ltp(symbol: str) -> float:
    quote = kite.ltp(f"NSE:{symbol}")
    return quote[f"NSE:{symbol}"]["last_price"]


def get_historical(symbol: str, interval="5minute", days=5):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    instruments = kite.instruments("NSE")
    instrument_token = next(
        i["instrument_token"] for i in instruments if i["tradingsymbol"] == symbol
    )

    data = kite.historical_data(
        instrument_token=instrument_token,
        from_date=from_date,
        to_date=to_date,
        interval=interval
    )

    return data