from fastapi import APIRouter


router = APIRouter()

WATCHLIST = ["INFY", "TCS", "HDFCBANK", "RELIANCE", "ICICIBANK"]


@router.get("/scan")
def scan_market(strategy: str):
    if strategy == "sma_fast":
        signals = ["INFY BUY"]
    elif strategy == "sma_mid":
        signals = ["TCS BUY"]
    elif strategy == "sma_slow":
        signals = []
    else:
        signals = []

    return {"signals": signals}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}