from kiteconnect import KiteConnect
import os

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

if not API_KEY or not API_SECRET:
    raise Exception("Zerodha API credentials missing. Set ZERODHA_API_KEY and ZERODHA_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

# Access token will be set AFTER login
def set_access_token(token: str):
    kite.set_access_token(token)


def place_real_order(symbol, qty, side):
    if not kite.access_token:
        return {"error": "Login with Zerodha first"}

    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol.upper(),
            transaction_type=kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" else kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )

        return {
            "status": "Order placed",
            "order_id": order_id,
            "symbol": symbol.upper(),
            "qty": qty,
            "side": side.upper()
        }

    except Exception as e:
        return {"error": str(e)}