from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from kiteconnect import KiteConnect
import os
import json
from datetime import datetime

# --- SURGICAL IMPORTS ---
from backend.strategy import dual_path_signal
from backend.data_provider import get_historical, get_ltp
from backend.config_loader import load_watchlist
from backend.indicators import calculate_adx
# ----------------------------

from backend.zerodha_session import (
    get_kite,
    get_login_url,
    save_access_token
)

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")
TRADES_FILE = "backend/data/active_trades.json"
HISTORY_FILE = "backend/data/trade_history.json"

# ==========================================
# 🚨 GLOBAL KITE INSTANCE (REQUIRED FOR MAIN.PY)
# ==========================================
kite = KiteConnect(api_key=API_KEY)

if ACCESS_TOKEN:
    try:
        kite.set_access_token(ACCESS_TOKEN)
        print("✅ Global Zerodha Session Initialized.")
    except Exception as e:
        print(f"⚠️ Token auto-load failed: {e}")
# ==========================================

router = APIRouter()

# --------------------------------------------------
# PERSISTENCE & HISTORY HELPERS
# --------------------------------------------------
def load_trades():
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
    os.makedirs(os.path.dirname(TRADES_FILE), exist_ok=True)
    serializable = {}
    for sym, details in trades.items():
        copy = details.copy()
        copy["entry_date"] = details["entry_date"].isoformat()
        serializable[sym] = copy
    with open(TRADES_FILE, "w") as f:
        json.dump(serializable, f, indent=4)

def save_to_history(trade_data):
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
# UPDATED MARKET SCANNER
# --------------------------------------------------
@router.get("/scan")
def scan(
    st_p: int = 10, st_m: float = 3.0, 
    ema_f: int = 9, ema_s: int = 21, 
    adx: float = 25.0, rsi: float = 40.0
):
    watchlist = load_watchlist()
    results = []
    
    for symbol in watchlist:
        try:
            df = get_historical(symbol) 
            
            if df is None or df.empty: continue
            
            signal, current_adx = dual_path_signal(df, st_p, st_m, ema_f, ema_s, adx, rsi)
            price = get_ltp(symbol)
            
            if signal in ["BUY", "SELL"]:
                results.append({
                    "symbol": symbol,
                    "price": round(price, 2),
                    "signal": signal,
                    "adx": round(current_adx, 2)
                })
        except Exception as e:
            print(f"⚠️ Scan failed for {symbol}: {e}")
            continue
            
    return results

# --------------------------------------------------
# STABLE ENDPOINTS 
# --------------------------------------------------
@router.get("/auto-sell")
def auto_sell():
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
                closed_trade = {
                    "symbol": symbol, "entry_price": trade["entry_price"],
                    "exit_price": round(current_price, 2), "quantity": trade["quantity"],
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
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

@router.get("/balance")
def balance():
    try:
        local_kite = get_kite()
        m = local_kite.margins()["equity"]
        return {
            "available_cash": round(m["available"]["cash"], 2),
            "total_balance": round(m["net"], 2)
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
    local_kite = get_kite()
    t_type = local_kite.TRANSACTION_TYPE_BUY if side.upper() == "BUY" else local_kite.TRANSACTION_TYPE_SELL
    oid = local_kite.place_order(
        variety=local_kite.VARIETY_REGULAR, exchange=local_kite.EXCHANGE_NSE,
        tradingsymbol=symbol, transaction_type=t_type,
        quantity=quantity, order_type=local_kite.ORDER_TYPE_LIMIT,
        price=price, product=local_kite.PRODUCT_CNC
    )
    return {"status": "SUCCESS", "order_id": oid}