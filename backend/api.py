from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from backend.zerodha_trader import kite, API_SECRET, set_access_token, place_real_order

router = APIRouter()

# ---------- Zerodha Login Flow ----------

@router.get("/zerodha/login")
def zerodha_login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


@router.get("/zerodha/callback")
def zerodha_callback(request_token: str):
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    set_access_token(data["access_token"])
    return {"message": "Zerodha login successful. You can now trade."}


# ---------- Market Scan (Demo Signals) ----------

@router.get("/scan")
def scan_market(strategy: str = "crossover"):
    """
    Scan market and return BUY signals only
    strategy = crossover | price | triple
    """

    signals = []

    # Fake demo logic (replace later with real SMA calc)
    if strategy == "crossover":
        signals.append("INFY BUY (SMA Cross)")
    elif strategy == "price":
        signals.append("HDFCBANK BUY (Price > SMA)")
    elif strategy == "triple":
        signals.append("RELIANCE BUY (Triple SMA Trend)")

    return {"signals": signals}


# ---------- Place Order ----------

class OrderRequest(BaseModel):
    symbol: str
    quantity: int
    side: str  # BUY or SELL


@router.post("/order")
def place_order(order: OrderRequest):
    return place_real_order(order.symbol, order.quantity, order.side)


# ---------- Bot Status ----------

@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}