from kiteconnect import KiteConnect
import os

API_KEY = os.getenv("ZERODHA_API_KEY")
ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN")

if not API_KEY or not ACCESS_TOKEN:
    raise Exception("Zerodha API credentials missing. Check environment variables.")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)


def place_real_order(symbol: str, qty: int, side: str):
    if qty > 5:
        return {"error": "Max qty allowed is 5"}

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