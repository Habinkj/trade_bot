from fastapi import APIRouter
from backend.data_provider import get_historical
from backend.strategy import sma_signal, ema_signal
from backend.config_loader import load_watchlist

router = APIRouter()

@router.get("/scan")
def scan_market(strategy: str = "sma"):
    watchlist = load_watchlist()
    results = []

    for symbol in watchlist:
        try:
            df = get_historical(symbol)

            if strategy == "sma":
                signal = sma_signal(df)
            else:
                signal = ema_signal(df)

            if signal == "BUY":
                results.append(symbol)

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results