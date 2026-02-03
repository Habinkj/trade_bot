from kiteconnect import KiteConnect
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def get_candles(instrument_token):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=5)

    data = kite.historical_data(
        instrument_token=instrument_token,
        from_date=from_date,
        to_date=to_date,
        interval="5minute"
    )

    return data

#------- trailing stop loss --------

def manage_trailing_sl(symbol, entry_price):
    trail_percent = 1.5  # Example 1.5%
    stop_price = entry_price * (1 - trail_percent / 100)

    # Continuously monitor LTP
    # If price drops to stop_price → place SELL