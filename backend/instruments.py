from backend.zerodha_session import get_kite

instrument_map = {}

def load_instruments():
    global instrument_map
    kite = get_kite()
    instruments = kite.instruments("NSE")

    instrument_map = {
        inst["tradingsymbol"]: inst["instrument_token"]
        for inst in instruments
    }

def get_token(symbol: str):
    if not instrument_map:
        load_instruments()
    token = instrument_map.get(symbol)
    if not token:
        raise Exception(f"Token not found for {symbol}")
    return token

def get_token(symbol):
    kite = get_kite()
    instruments = kite.instruments("NSE")

    for inst in instruments:
        if inst["tradingsymbol"] == symbol:
            return inst["instrument_token"]

    raise Exception(f"Token not found for {symbol}")