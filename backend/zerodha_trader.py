import pandas as pd
from kiteconnect import KiteConnect
import os
from backend.zerodha_session import get_access_token
from backend.instruments import get_token


def get_kite():
    api_key = os.getenv("ZERODHA_API_KEY")
    access_token = get_access_token()

    if not access_token:
        raise Exception("User not logged in to Zerodha")

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite


def get_historical(symbol, interval="5minute", days=5):
    kite = get_kite()
    token = get_token(symbol)

    from datetime import datetime, timedelta
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    candles = kite.historical_data(token, from_date, to_date, interval)

    df = pd.DataFrame(candles)
    return df