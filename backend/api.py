from fastapi import APIRouter
from backend.zerodha_trader import check_strategy

router = APIRouter()

WATCHLIST = ["INFY", "TCS", "HDFCBANK", "RELIANCE", "ICICIBANK"]


@router.get("/scan")
def scan_market(strategy: str = "crossover"):
    signals = []

    for symbol in WATCHLIST:
        result = check_strategy(symbol, strategy)
        if result:
            signals.append(result)

    return {"signals": signals}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}