from fastapi import APIRouter
from backend.strategy import generate_signal
from backend.utils import load_config, get_dhan_credentials
from backend.trader import DhanTrader

router = APIRouter()

@router.get("/signal/{symbol}")
def get_signal(symbol: str):
    return generate_signal(symbol)

@router.post("/trade/{symbol}")
def execute_trade(symbol: str):
    cfg = load_config()
    creds = get_dhan_credentials()

    trader = DhanTrader(
        client_id=creds["client_id"],
        access_token=creds["access_token"],
        dry_run=cfg["app"]["dry_run"]
    )

    return {
        "status": "Trade request received",
        "mode": "DRY_RUN" if cfg["app"]["dry_run"] else "LIVE"
    }
