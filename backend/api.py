from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os
from datetime import datetime

from backend.indicators import calculate_adx
from backend.zerodha_session import (
    get_kite,
    get_login_url,
    save_access_token
)
from backend.data_provider import get_historical, get_ltp
from backend.strategy import (
    sma_dynamic_signal,
    ema_cross_signal,
    supertrend_signal
)
from backend.config_loader import load_watchlist

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

router = APIRouter()

# Global dictionary to track trades
# Now includes 'entry_date' to calculate holding period
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
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    save_access_token(data["access_token"])
    return {"status": "Login successful. You can close this tab."}


# --------------------------------------------------
# MARKET SCAN (Daily Timeframe)
# --------------------------------------------------

@router.get("/scan")
def scan(strategy: str, request: Request):
    try:
        get_kite()
    except Exception:
        return JSONResponse(status_code=401, content={"login_url": get_login_url()})

    watchlist = load_watchlist()
    results = []

    for symbol in watchlist:
        try:
            df = get_historical(symbol) # Fetches daily data
            adx_value = calculate_adx(df).iloc[-1]

            if strategy == "sma":
                fast = int(request.query_params.get("fast", 5))
                slow = int(request.query_params.get("slow", 10))
                if fast <= 0 or slow <= 0 or fast >= slow: continue
                signal = sma_dynamic_signal(df, fast, slow)
            elif strategy == "ema":
                signal = ema_cross_signal(df)
            elif strategy == "supertrend":
                signal = supertrend_signal(df)
            else:
                continue

            # ADX > 25 confirms a strong swing trend
            if signal == "BUY" and adx_value > 25:
                results.append({
                    "symbol": symbol,
                    "price": round(df["close"].iloc[-1], 2),
                    "signal": signal,
                    "adx": round(adx_value, 2)
                })
        except Exception as e:
            print(f"Scan error for {symbol}: {e}")

    return sorted(results, key=lambda x: x["adx"], reverse=True)[:3]


# --------------------------------------------------
# PLACE ORDER (CNC for Swing Trading)
# --------------------------------------------------

@router.post("/order")
def place_order(payload: dict):
    required_fields = ["symbol", "quantity", "min_price", "max_price"]
    if not all(k in payload for k in required_fields):
        return JSONResponse(status_code=400, content={"reason": "Invalid payload"})

    symbol = payload["symbol"]
    quantity = int(payload["quantity"])
    min_price, max_price = float(payload["min_price"]), float(payload["max_price"])
    side = payload.get("side", "BUY")

    try:
        current_price = get_ltp(symbol)
        if not (min_price <= current_price <= max_price):
            return {"status": "REJECTED", "reason": "Price out of allowed range"}

        result = place_trade(symbol, quantity, side)

        if side.upper() == "BUY":
            # entry_date allows the bot to count days held
            ACTIVE_TRADES[symbol] = {
                "entry_price": current_price,
                "quantity": quantity,
                "entry_date": datetime.now(), 
                "sold": False
            }
        return result
    except Exception as e:
        return JSONResponse(status_code=400, content={"reason": str(e)})


# --------------------------------------------------
# AUTO SELL (Price Targets + Time-Based Exit)
# --------------------------------------------------

@router.get("/auto-sell")
def auto_sell():
    results = []
    MAX_HOLDING_DAYS = 6  # Time-based exit for swing trading

    for symbol, trade in list(ACTIVE_TRADES.items()):
        if trade.get("sold"): continue

        try:
            current_price = get_ltp(symbol)
            entry_price = trade["entry_price"]
            change = (current_price - entry_price) / entry_price * 100
            
            # Days calculation
            days_held = (datetime.now() - trade["entry_date"]).days

            reason = None
            
            # 1. Take Profit (10%)
            if change >= 10:
                reason = "TARGET HIT"
            # 2. Stop Loss (5%)
            elif change <= -5:
                reason = "STOPLOSS HIT"
            # 3. Time-based Exit (Swing duration complete)
            elif days_held >= MAX_HOLDING_DAYS:
                reason = f"TIME LIMIT REACHED ({MAX_HOLDING_DAYS} Days)"

            if reason:
                place_trade(symbol, trade["quantity"], "SELL")
                results.append({
                    "symbol": symbol,
                    "exit_price": round(current_price, 2),
                    "reason": reason,
                    "days_held": days_held
                })
                trade["sold"] = True
                del ACTIVE_TRADES[symbol]
                
        except Exception as e:
            print(f"Auto-sell failed for {symbol}: {e}")
            continue

    return results


# --------------------------------------------------
# ACTIVE TRADES (Frontend Endpoint)
# --------------------------------------------------

@router.get("/trades")
def get_trades():
    results = []
    for symbol, trade in ACTIVE_TRADES.items():
        try:
            current_price = get_ltp(symbol)
            days_held = (datetime.now() - trade["entry_date"]).days
            pnl = ((current_price - trade["entry_price"]) / trade["entry_price"]) * 100
            
            results.append({
                "symbol": symbol,
                "entry_price": round(trade["entry_price"], 2),
                "current_price": round(current_price, 2),
                "quantity": trade["quantity"],
                "days_held": days_held,
                "pnl": round(pnl, 2)
            })
        except: continue
    return results


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def place_trade(symbol: str, quantity: int, side: str):
    kite = get_kite()
    t_type = kite.TRANSACTION_TYPE_BUY if side.upper() == "BUY" else kite.TRANSACTION_TYPE_SELL

    # Using PRODUCT_CNC to allow overnight holding
    order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        transaction_type=t_type,
        quantity=quantity,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_CNC  
    )

    return {"status": f"{side.upper()}_ORDER_PLACED", "order_id": order_id}