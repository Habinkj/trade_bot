import json
import os

INSTRUMENT_FILE = "config/symbols.json"

def load_instruments():
    with open(INSTRUMENT_FILE, "r") as f:
        return json.load(f)

def get_token(symbol):
    instruments = load_instruments()
    return instruments.get(symbol)