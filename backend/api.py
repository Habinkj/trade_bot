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

@router.get("/scan")
def scan():
    return scan_market()

@router.post("/order")
def order(req: OrderRequest):
    return place_real_order(req.symbol, req.qty, req.side)