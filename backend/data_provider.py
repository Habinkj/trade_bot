import pandas as pd
import random

def fetch_intraday_data(symbol):
    data = {
        "open": [random.uniform(100, 200) for _ in range(100)],
        "high": [random.uniform(200, 250) for _ in range(100)],
        "low": [random.uniform(80, 120) for _ in range(100)],
        "close": [random.uniform(100, 200) for _ in range(100)],
    }
    return pd.DataFrame(data)