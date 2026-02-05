import os
from kiteconnect import KiteConnect

TOKEN_FILE = "access_token.txt"

def save_access_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def get_access_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()

def get_kite():
    api_key = os.getenv("ZERODHA_API_KEY")
    kite = KiteConnect(api_key=api_key)

    access_token = get_access_token()
    if not access_token:
        raise Exception("Login required")

    kite.set_access_token(access_token)
    return kite