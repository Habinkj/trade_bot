from fastapi import APIRouter
from backend.zerodha_trader import get_candles
from backend.strategy import sma_signal
from backend.instruments import get_token
from bacend.instrucments import WATCHLIST

router = APIRouter()


@router.get("/scan")
def scan_market(strategy: str):
    results = []

    for symbol in WATCHLIST:
        token = get_token(symbol)
        if not token:
            continue

        candles = get_candles(token)

        if strategy == "sma_fast":
            signal = sma_signal(candles, 5, 9)
        elif strategy == "sma_mid":
            signal = sma_signal(candles, 9, 21)
        elif strategy == "sma_slow":
            signal = sma_signal(candles, 5, 34)
        else:
            signal = None

        if signal == "BUY":
            price = candles[-1]["close"]
            results.append({
                "symbol": symbol,
                "price": price,
                "signal": "BUY"
            })

    return results