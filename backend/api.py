from fastapi import APIRouter
from backend.zerodha_trader import check_strategy

router = APIRouter()

WATCHLIST = ["INFY", "TCS", "HDFCBANK", "RELIANCE", "ICICIBANK"]


@router.get("/scan")
def scan_market(strategy: str):

    # Example dummy logic — replace with real data later
    if strategy == "sma_fast":
        signals = ["INFY BUY"]  # Fast signals more frequent
    elif strategy == "sma_mid":
        signals = ["TCS BUY"]
    elif strategy == "sma_slow":
        signals = []  # Slow signals rare
    else:
        signals = []

    return {"signals": signals}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}