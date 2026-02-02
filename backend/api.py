from fastapi import APIRouter
from zerodha_trader import kite  # your Zerodha session object

router = APIRouter()


# ---------------- BOT ENDPOINTS ---------------- #

@router.get("/scan")
def scan_market():
    """
    Scan market using Zerodha session
    """
    # Example signals (replace later with strategy logic)
    return {"signals": ["INFY BUY", "TCS SELL", "HDFCBANK BUY"]}


@router.post("/order")
def place_order(order: dict):
    """
    Place order via Zerodha
    """
    try:
        response = kite.place_order(
            variety="regular",
            exchange="NSE",
            tradingsymbol=order["symbol"],
            transaction_type="BUY" if order["side"] == "BUY" else "SELL",
            quantity=int(order["quantity"]),
            order_type="MARKET",
            product="MIS"
        )
        return {"status": "Order placed", "order_id": response}

    except Exception as e:
        return {"status": "Order failed", "error": str(e)}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}