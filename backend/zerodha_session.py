import os
from kiteconnect import KiteConnect

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

TOKEN_FILE = "access_token.txt"



def get_balance():
    margins = kite.margins()
    return {
        "available_cash": margins["equity"]["available"]["cash"],
        "used_margin": margins["equity"]["utilised"]["debits"],
        "net": margins["equity"]["net"]
    }

def get_login_url():
    kite = KiteConnect(api_key=API_KEY)
    return kite.login_url()


def save_access_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def get_access_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()


def get_kite():
    token = get_access_token()
    if not token:
        raise Exception("Login required")

    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(token)
    return kite