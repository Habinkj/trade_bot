import time
import pandas as pd
from datetime import datetime, timedelta
from backend.zerodha_session import get_kite
from backend.instruments import get_token

CACHE = {}
CACHE_EXPIRY = 300  # 5 minutes


def get_historical(symbol):
    now = time.time()

    # Return cached data if available
    if symbol in CACHE:
        df, timestamp = CACHE[symbol]
        if now - timestamp < CACHE_EXPIRY:
            return df

    kite = get_kite()
    instrument_token = get_token(symbol)

    to_date = datetime.now()
    from_date = to_date - timedelta(days=20)

    data = kite.historical_data(
        instrument_token,
        from_date,
        to_date,
        "day"
    )

    df = pd.DataFrame(data)

    # Save in cache
    CACHE[symbol] = (df, now)

    return df

def get_ltp(symbol):
    return kite.ltp(f"NSE:{symbol}")[f"NSE:+ {symbol}"]["last_price"]