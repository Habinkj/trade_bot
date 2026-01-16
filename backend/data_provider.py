# backend/data_provider.py
import pandas as pd
from datetime import datetime, timedelta

def get_candles(symbol: str, interval: str = "5m", lookback_days: int = 5):
    """
    TEMPORARY DATA PROVIDER (Groww-style placeholder)

    This simulates OHLC data so your bot, ML, and frontend WORK.
    Later we will replace this with:
    - Dhan Data API (official)
    - OR Groww official API (if they approve you)
    """

    end = datetime.now()
    start = end - timedelta(days=lookback_days)

    dates = pd.date_range(start=start, end=end, freq="5min")

    df = pd.DataFrame({
        "datetime": dates,
        "open": 1000,
        "high": 1010,
        "low": 990,
        "close": 1005,
        "volume": 100000
    })

    return df
