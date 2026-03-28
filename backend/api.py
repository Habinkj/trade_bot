import signal
from unittest import result

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os

from backend.indicators import calculate_adx
from backend.zerodha_session import (
    get_kite,
    get_login_url,
    save_access_token
)
from backend.data_provider import get_historical
from backend.strategy import (
    sma_dynamic_signal,
    ema_cross_signal,
    supertrend_signal
)
from backend.config_loader import load_watchlist


API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

router = APIRouter()
ACTIVE_TRADES = {}

# --------------------------------------------------
# LOGIN FLOW
# --------------------------------------------------

@router.get("/login")
def login():
    return RedirectResponse(get_login_url())


@router.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    kite = KiteConnect(api_key=API_KEY)

    data = kite.generate_session(
        request_token,
        api_secret=API_SECRET
    )

    save_access_token(data["access_token"])

    return {"status": "Login successful. You can close this tab."}


# --------------------------------------------------
# MARKET SCAN
# --------------------------------------------------

@router.get("/scan")
def scan(strategy: str, request: Request):
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

            # 🔥 ADX FOR ALL STRATEGIES
            adx = calculate_adx(df)
            adx_value = adx.iloc[-1]
            strength = "STRONG" if adx_value > 25 else "WEAK"

            # 🔥 STRATEGY SELECTION
            if strategy == "sma":
                fast = int(request.query_params.get("fast", 5))
                slow = int(request.query_params.get("slow", 10))

                # safety check
                if fast <= 0 or slow <= 0 or fast >= slow:
                    continue

                signal = sma_dynamic_signal(df, fast, slow)

            elif strategy == "ema":
                signal = ema_cross_signal(df)

            elif strategy == "supertrend":
                signal = supertrend_signal(df)

            else:
                continue

            # 🔥 ONLY RETURN VALID SIGNALS
            # add results
            if signal == "BUY" and adx_value > 25:
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal,
                    "adx": round(adx_value, 2),
                    "strength": strength
                })


            results = sorted(results, key=lambda x: x["adx"], reverse=True)

            results = results[:3]


            return results


# --------------------------------------------------
# BALANCE
# --------------------------------------------------

@router.get("/balance")
def balance():
    kite = get_kite()
    margins = kite.margins()["equity"]

    return {
        "available_cash": margins["available"]["cash"]
    }


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

    # PRICE SAFETY CHECK
    if current_price < min_price or current_price > max_price:
        return {
            "status": "REJECTED",
            "reason": "Price out of allowed range",
            "current_price": current_price
        }

    result = place_trade(symbol, quantity, side)

# 🔥 SAVE TRADE AFTER BUY
    if side.upper() == "BUY":
        ACTIVE_TRADES[symbol] = {
            "entry_price": get_ltp(symbol),
            "quantity": quantity
        }

    return result

@router.get("/auto-sell")
def auto_sell():
    results = []

    for symbol, trade in list(ACTIVE_TRADES.items()):
        current_price = get_ltp(symbol)
        entry_price = trade["entry_price"]

        change = (current_price - entry_price) / entry_price * 100

        # 🔥 EXIT CONDITIONS
        if change >= 4:
            reason = "TARGET HIT"
        elif change <= -2:
            reason = "STOPLOSS HIT"
        else:
            continue

        # 🔥 PLACE SELL ORDER
        order = place_trade(symbol, trade["quantity"], "SELL")

        results.append({
            "symbol": symbol,
            "exit_price": round(current_price, 2),
            "reason": reason
        })

        # 🔥 REMOVE TRADE AFTER SELL
        del ACTIVE_TRADES[symbol]

    return results
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