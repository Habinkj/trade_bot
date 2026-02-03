from fastapi import APIRouter


router = APIRouter()

WATCHLIST = ["INFY", "TCS", "HDFCBANK", "RELIANCE", "ICICIBANK"]


@router.get("/scan")
def scan_market(strategy: str):
    """
    Returns BUY signals based on selected SMA strategy
    """

    if strategy == "sma_fast":
        # Fast SMA → more signals
        signals = ["INFY BUY", "ICICIBANK BUY"]

    elif strategy == "sma_mid":
        # Medium SMA → moderate signals
        signals = ["TCS BUY"]

    elif strategy == "sma_slow":
        # Slow SMA → rare but stronger signals
        signals = ["HDFCBANK BUY"]

    else:
        signals = []

    return {"signals": signals}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}