from fastapi import APIRouter
from backend.zerodha_trader import kite  # your Zerodha session object
from bckend.zerodha_trader import place_real_order
router = APIRouter()


# ---------------- BOT ENDPOINTS ---------------- #

@router.get("/scan")
def scan_market():
    """
    Scan market using Zerodha session
    """
    # Example signals (replace later with strategy logic)
    return {"signals": ["INFY BUY", "TCS SELL", "HDFCBANK BUY"]}


from backend.zerodha_trader import place_real_order

@router.post("/order")
def place_order(order: dict):
    result = place_real_order(order["symbol"], order["qty"], order["side"])

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}