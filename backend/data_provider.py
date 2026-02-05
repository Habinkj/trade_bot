import pandas as pd
from datetime import datetime, timedelta
from backend.zerodha_session import get_kite
from backend.instruments import get_token

def get_historical(symbol, interval="5minute", days=5):
    kite = get_kite()   # ✅ INSIDE function (only runs after login)
    token = get_token(symbol)

    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    candles = kite.historical_data(token, from_date, to_date, interval)
    df = pd.DataFrame(candles)
    return df