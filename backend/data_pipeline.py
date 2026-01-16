import pandas as pd
from dhanhq import dhanhq
import os

def fetch_and_store(symbol, security_id, dhan):
    data = dhan.historical_daily_data(
        security_id=security_id,
        exchange_segment=dhanhq.NSE,
        instrument_type="EQUITY",
        from_date="2024-01-01",
        to_date="2025-01-01"
    )

    df = pd.DataFrame(data["data"])
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(f"data/raw/{symbol}.csv", index=False)
    return df
