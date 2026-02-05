from backend.zerodha_session import get_kite

instrument_map = {}

def load_instruments():
    global instrument_map
    kite = get_kite()
    instruments = kite.instruments("NSE")

    instrument_map = {inst["tradingsymbol"]: inst["instrument_token"] for inst in instruments}

def get_token(symbol: str):
    if not instrument_map:
        load_instruments()
    return instrument_map.get(symbol)