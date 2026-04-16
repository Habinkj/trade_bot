import time
import pandas as pd
from datetime import datetime, timedelta
from backend.zerodha_session import get_kite
from backend.instruments import get_token

CACHE = {}
CACHE_EXPIRY = 3600  # 1 hour cache for daily data


def get_historical(symbol):
    now = time.time()

    if symbol in CACHE:
        df, timestamp = CACHE[symbol]
        if now - timestamp < CACHE_EXPIRY:
            return df

    kite = get_kite()
    instrument_token = get_token(symbol)

    to_date = datetime.now()
    # Swing trading needs ~200 days for stability
    from_date = to_date - timedelta(days=200)

    data = kite.historical_data(
        instrument_token,
        from_date,
        to_date,
        "day" # Changed from 5minute to day
    )

    df = pd.DataFrame(data)
    CACHE[symbol] = (df, now)

    return df

def get_ltp(symbol):
    kite = get_kite()
    ltp_data = kite.ltp([f"NSE:{symbol}"])
    return ltp_data[f"NSE:{symbol}"]["last_price"]