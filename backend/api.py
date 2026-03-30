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

            adx = calculate_adx(df)
            adx_value = adx.iloc[-1]
            strength = "STRONG" if adx_value > 25 else "WEAK"

            if strategy == "sma":
                fast = int(request.query_params.get("fast", 5))
                slow = int(request.query_params.get("slow", 10))

                if fast <= 0 or slow <= 0 or fast >= slow:
                    continue

                signal = sma_dynamic_signal(df, fast, slow)

            elif strategy == "ema":
                signal = ema_cross_signal(df)

            elif strategy == "supertrend":
                signal = supertrend_signal(df)

            else:
                continue

            if signal == "BUY" and adx_value > 25:
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal,
                    "adx": round(adx_value, 2),
                    "strength": strength
                })

        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    # SORT + TOP 3
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
        "available_cash": margins["available"]["cash"],
        "total_balance": margins["net"]
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
    side = payload.get("side", "BUY")

    current_price = get_ltp(symbol)

    # PRICE SAFETY CHECK
    if current_price < min_price or current_price > max_price:
        return {
            "status": "REJECTED",
            "reason": "Price out of allowed range",
            "current_price": current_price
        }

    result = place_trade(symbol, quantity, side)

    # SAVE TRADE
    if side.upper() == "BUY":
        ACTIVE_TRADES[symbol] = {
            "entry_price": current_price,   # ✅ FIXED
            "quantity": quantity,
            "sold": False                  # ✅ SAFETY FLAG
        }

    return result


# --------------------------------------------------
# AUTO SELL ENGINE
# --------------------------------------------------

@router.get("/auto-sell")
def auto_sell():
    results = []

    for symbol, trade in list(ACTIVE_TRADES.items()):

        # prevent duplicate sell
        if trade.get("sold"):
            continue

        current_price = get_ltp(symbol)
        entry_price = trade["entry_price"]

        change = (current_price - entry_price) / entry_price * 100

        # EXIT CONDITIONS
        if change >= 4:
            reason = "TARGET HIT"
        elif change <= -2:
            reason = "STOPLOSS HIT"
        else:
            continue

        try:
            order = place_trade(symbol, trade["quantity"], "SELL")
            print("AUTO SELL:", symbol, reason)
        except Exception as e:
            print("Sell failed:", e)
            continue

        results.append({
            "symbol": symbol,
            "exit_price": round(current_price, 2),
            "reason": reason
        })

        # mark + remove
        trade["sold"] = True
        del ACTIVE_TRADES[symbol]

    return results


# --------------------------------------------------
# ACTIVE TRADES VIEW
# --------------------------------------------------

@router.get("/trades")
def get_trades():
    results = []

    for symbol, trade in ACTIVE_TRADES.items():
        current_price = get_ltp(symbol)
        entry_price = trade["entry_price"]
        qty = trade["quantity"]

        pnl = ((current_price - entry_price) / entry_price) * 100

        results.append({
            "symbol": symbol,
            "entry_price": round(entry_price, 2),
            "current_price": round(current_price, 2),
            "quantity": qty,
            "pnl": round(pnl, 2)
        })

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