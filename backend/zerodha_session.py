import os
from kiteconnect import KiteConnect

API_KEY = os.getenv("ZERODHA_API_KEY")
_access_token = None

def save_access_token(token):
    global _access_token
    _access_token = token

def get_kite():
    global _access_token
    if not _access_token:
        raise Exception("Login required")

    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(_access_token)
    return kite