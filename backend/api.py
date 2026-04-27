from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os
import json
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
TRADES_FILE = "backend/data/active_trades.json"
HISTORY_FILE = "backend/data/trade_history.json"

router = APIRouter()

# --------------------------------------------------
# PERSISTENCE & HISTORY HELPERS
# --------------------------------------------------

def load_trades():
    """Loads active trades for the risk engine."""
    if os.path.exists(TRADES_FILE):
        try:
            with open(TRADES_FILE, "r") as f:
                content = f.read().strip()
                if not content: return {}
                data = json.loads(content)
                for sym in data:
                    data[sym]["entry_date"] = datetime.fromisoformat(data[sym]["entry_date"])
                return data
        except Exception as e:
            print(f"Error loading trades: {e}")
    return {}

def save_trades(trades):
    """Saves active trades to JSON."""
    os.makedirs(os.path.dirname(TRADES_FILE), exist_ok=True)
    serializable = {}
    for sym, details in trades.items():
        copy = details.copy()
        copy["entry_date"] = details["entry_date"].isoformat()
        serializable[sym] = copy
    with open(TRADES_FILE, "w") as f:
        json.dump(serializable, f, indent=4)

def save_to_history(trade_data):
    """Appends a closed trade to the permanent history file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except: history = []
    
    trade_data["exit_date"] = datetime.now().isoformat()
    history.append(trade_data)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

ACTIVE_TRADES = load_trades()

# --------------------------------------------------
# MARKET SCANNER (DYNAMIC)
# --------------------------------------------------

@router.get("/scan")
def scan(strategy: str, fast: int, slow: int):
    """Runs scanning logic with user-defined periods."""
    watchlist = load_watchlist()
    results = []
    
    for symbol in watchlist:
        try:
            df = get_historical(symbol)
            
            if strategy.lower() == "supertrend":
                signal = supertrend_signal(df, period=fast, multiplier=slow) 
            elif strategy.lower() == "ema":
                signal = ema_cross_signal(df, fast_period=fast, slow_period=slow)
            else:
                signal = sma_dynamic_signal(df, fast, slow)
            
            adx_val = calculate_adx(df).iloc[-1]
            price = get_ltp(symbol)
            
            results.append({
                "symbol": symbol,
                "price": round(price, 2),
                "signal": signal,
                "adx": round(adx_val, 2)
            })
        except Exception as e:
            print(f"⚠️ Scan failed for {symbol}: {e}")
            continue
            
    return results

# --------------------------------------------------
# RISK ENGINE & HISTORY
# --------------------------------------------------

@router.get("/auto-sell")
def auto_sell():
    """Monitors 2% Trailing SL and 5-Day Exit, then saves to history."""
    results = []
    for symbol, trade in list(ACTIVE_TRADES.items()):
        try:
            current_price = get_ltp(symbol)
            if current_price > trade.get("peak_price", 0):
                trade["peak_price"] = current_price
                save_trades(ACTIVE_TRADES) 

            drop_from_peak = ((trade["peak_price"] - current_price) / trade["peak_price"]) * 100
            days_held = (datetime.now() - trade["entry_date"]).days

            reason = None
            if drop_from_peak >= 2.0: reason = "TRAILING SL (2%)"
            elif days_held >= 5: reason = "5-DAY LIMIT"

            if reason:
                place_trade(symbol, trade["quantity"], "SELL", current_price)
                
                # Create history object
                closed_trade = {
                    "symbol": symbol,
                    "entry_price": trade["entry_price"],
                    "exit_price": round(current_price, 2),
                    "quantity": trade["quantity"],
                    "pnl": round(((current_price - trade["entry_price"]) / trade["entry_price"]) * 100, 2),
                    "reason": reason
                }
                
                save_to_history(closed_trade)
                results.append(closed_trade)
                del ACTIVE_TRADES[symbol]
                save_trades(ACTIVE_TRADES)
                
        except: continue
    return results

@router.get("/history")
def get_history():
    """Fetches past trade history."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# --------------------------------------------------
# ACCOUNT & LIVE BALANCE
# --------------------------------------------------

@router.get("/balance")
def balance():
    """Matches Kite Mobile App display (Total Equity)."""
    try:
        kite = get_kite()
        m = kite.margins()["equity"]
        
        # 'net' represents the Total Opening Balance/Equity
        total_balance = m["net"] 
        available_cash = m["available"]["cash"]

        return {
            "available_cash": round(available_cash, 2),
            "total_balance": round(total_balance, 2)
        }
    except:
        return {"available_cash": 0, "total_balance": 0}

@router.get("/trades")
def get_trades():
    results = []
    for symbol, trade in list(ACTIVE_TRADES.items()):
        try:
            cp = get_ltp(symbol)
            results.append({
                "symbol": symbol,
                "entry_price": round(trade["entry_price"], 2),
                "peak_price": round(trade.get("peak_price", trade["entry_price"]), 2),
                "current_price": round(cp, 2),
                "quantity": trade["quantity"],
                "pnl": round(((cp - trade["entry_price"]) / trade["entry_price"]) * 100, 2)
            })
        except: continue
    return results

# --------------------------------------------------
# ORDERS & AUTH
# --------------------------------------------------

@router.post("/order")
def place_order(payload: dict):
    symbol, qty, side = payload["symbol"], int(payload["quantity"]), payload.get("side", "BUY")
    try:
        cp = get_ltp(symbol)
        res = place_trade(symbol, qty, side, cp)
        if side.upper() == "BUY":
            ACTIVE_TRADES[symbol] = {
                "entry_price": cp, "peak_price": cp, "quantity": qty, 
                "entry_date": datetime.now(), "sold": False
            }
            save_trades(ACTIVE_TRADES)
        return res
    except Exception as e:
        return JSONResponse(status_code=400, content={"reason": str(e)})

def place_trade(symbol: str, quantity: int, side: str, price: float):
    kite = get_kite()
    t_type = kite.TRANSACTION_TYPE_BUY if side.upper() == "BUY" else kite.TRANSACTION_TYPE_SELL
    oid = kite.place_order(
        variety=kite.VARIETY_REGULAR, exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol, transaction_type=t_type,
        quantity=quantity, order_type=kite.ORDER_TYPE_LIMIT,
        price=price, product=kite.PRODUCT_CNC
    )
    return {"status": "SUCCESS", "order_id": oid}

@router.get("/login")
def login(): return RedirectResponse(get_login_url())

@router.get("/callback")
def callback(request: Request):
    token = request.query_params.get("request_token")
    data = get_kite().generate_session(token, api_secret=API_SECRET)
    save_access_token(data["access_token"])
    return {"status": "Login successful"}