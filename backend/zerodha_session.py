import os
import json
from kiteconnect import KiteConnect

TOKEN_FILE = "backend/data/session.json"

def save_access_token(access_token: str):
    """Save access token to file after login"""
    os.makedirs("backend/data", exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": access_token}, f)


def load_access_token():
    """Load saved access token"""
    if not os.path.exists(TOKEN_FILE):
        return None

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        return data.get("access_token")


def get_kite():
    """
    Create Kite session safely.
    Will not crash server if user not logged in yet.
    """
    api_key = os.getenv("ZERODHA_API_KEY")
    if not api_key:
        raise Exception("ZERODHA_API_KEY not set")

    kite = KiteConnect(api_key=api_key)

    access_token = load_access_token()
    if not access_token:
        raise Exception("Login required")

    kite.set_access_token(access_token)
    return kite