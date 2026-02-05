from kiteconnect import KiteConnect
import os

kite = None

def create_session(request_token: str):
    global kite

    api_key = os.getenv("KITE_API_KEY")
    api_secret = os.getenv("KITE_API_SECRET")

    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])

    print("✅ Zerodha session created")

def get_kite():
    if kite is None:
        raise Exception("Kite session not initialized. Please login.")
    return kite