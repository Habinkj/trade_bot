from fastapi import APIRouter
from pydantic import BaseModel
from backend.strategy import generate_signal, scan_market
from backend.zerodha_trader import place_real_order

router = APIRouter()

class PredictRequest(BaseModel):
    symbol: str
    mode: str = "DEFAULT"

class OrderRequest(BaseModel):
    symbol: str
    qty: int
    side: str

@router.post("/predict")
def predict(req: PredictRequest):
    return generate_signal(req.symbol, req.mode)

@app.get("/scan")
def scan_market():
    signals = strategy.scan()  # your existing signal list

    results = []

    for symbol in signals:
        try:
            price = broker.get_ltp(symbol)  # fetch live price
        except:
            price = "N/A"

        results.append({
            "symbol": symbol,
            "price": price
        })

    return {"signals": results}

@router.post("/order")
def order(req: OrderRequest):
    return place_real_order(req.symbol, req.qty, req.side)

@app.get("/status")
def strategy_status():
    return {"running": True}