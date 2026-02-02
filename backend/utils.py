from kiteconnect import KiteConnect
import os
import json

KITE_API_KEY = os.getenv("KITE_API_KEY")


def load_instrument_tokens():
    """
    Download full instrument list from Zerodha and build a symbol → token map
    """
    kite = KiteConnect(api_key=KITE_API_KEY)
    instruments = kite.instruments("NSE")

    token_map = {}

    for ins in instruments:
        symbol = ins["tradingsymbol"]
        token = ins["instrument_token"]
        token_map[symbol] = token

    return token_map


# Load once at startup
SYMBOL_TOKEN_MAP = load_instrument_tokens()