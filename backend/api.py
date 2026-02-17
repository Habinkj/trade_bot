from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os

from backend.zerodha_session import (
    get_kite,
    get_login_url,
    save_access_token
)
from backend.data_provider import get_historical
from backend.strategy import (
    sma_5_10_signal,
    sma_9_21_signal,
    sma_15_20_signal,
    ema_cross_signal
)
from backend.config_loader import load_watchlist

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

router = APIRouter()

# --------------------------------------------------
# LOGIN FLOW
# --------------------------------------------------

@router.get("/login")
def login():
    return RedirectResponse(get_login_url())


@router.get("/callback")
def callback(request_token: str):
    kite = KiteConnect(api_key=API_KEY)
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    save_access_token(data["access_token"])
    return {"status": "Login successful. You can close this tab."}


# --------------------------------------------------
# MARKET SCAN
# --------------------------------------------------

@router.get("/scan")
def scan(strategy: str):
    try:
        get_kite()
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"login_url": get_login_url()}
        )

    watchlist = load_watchlist()
    results = []

    for symbol in watchlist:
        try:
            df = get_historical(symbol)

            if strategy == "sma_5_10":
                signal = sma_5_10_signal(df)
            elif strategy == "sma_9_21":
                signal = sma_9_21_signal(df)
            elif strategy == "sma_15_20":
                signal = sma_15_20_signal(df)
            elif strategy == "ema_cross":
                signal = ema_cross_signal(df)
            else:
                continue

            if signal == "BUY":
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal
                })

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return results


# --------------------------------------------------
# BALANCE
# --------------------------------------------------

@router.get("/balance")
def balance():
    try:
        kite = get_kite()
        margins = kite.margins()["equity"]
        return {
            "available_cash": margins["available"]["cash"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Balance fetch failed: {str(e)}"
        )


# --------------------------------------------------
# PLACE ORDER (BUY / SELL)
# --------------------------------------------------

@router.post("/order")
def place_order(payload: dict):
    symbol = payload["symbol"]
    quantity = int(payload["quantity"])
    min_price = float(payload["min_price"])
    max_price = float(payload["max_price"])
    side = payload.get("side", "BUY")  # BUY or SELL

    current_price = get_ltp(symbol)

    # ✅ PRICE SAFETY CHECK
    if current_price < min_price or current_price > max_price:
        return {
            "status": "REJECTED",
            "reason": "Price out of allowed range",
            "current_price": current_price
        }

    return place_trade(symbol, quantity, side)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def get_ltp(symbol: str):
    kite = get_kite()
    ltp_data = kite.ltp([f"NSE:{symbol}"])
    return ltp_data[f"NSE:{symbol}"]["last_price"]


def place_trade(symbol: str, quantity: int, side: str):
    kite = get_kite()

    transaction_type = (
        kite.TRANSACTION_TYPE_BUY
        if side.upper() == "BUY"
        else kite.TRANSACTION_TYPE_SELL
    )

    order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_CNC
    )

    return {
        "status": f"{side.upper()}_ORDER_PLACED",
        "order_id": order_id
    }