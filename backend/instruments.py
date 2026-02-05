from backend.zerodha_session import get_kite

def get_token(symbol: str):
    kite = get_kite()

    instruments = kite.instruments("NSE")  # Only NSE instruments

    symbol = symbol.upper().strip()

    for inst in instruments:
        if inst["tradingsymbol"] == symbol and inst["exchange"] == "NSE":
            return inst["instrument_token"]

    raise Exception(f"Token not found for {symbol}")