from backend.zerodha_session import get_kite

# Cache instruments so we don't download every time
_instruments_cache = None

def _load_instruments():
    global _instruments_cache
    if _instruments_cache is None:
        kite = get_kite()
        _instruments_cache = kite.instruments("NSE")
    return _instruments_cache


def get_token(symbol: str):
    symbol = symbol.upper().strip()
    instruments = _load_instruments()

    for inst in instruments:
        if inst["tradingsymbol"] == symbol and inst["exchange"] == "NSE":
            return inst["instrument_token"]

    raise Exception(f"Token not found for {symbol}")