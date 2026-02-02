import os
from kiteconnect import KiteConnect

class BrokerAPI:
    def __init__(self):
        self.api_key = os.getenv("KITE_API_KEY")
        self.api_secret = os.getenv("KITE_API_SECRET")
        self.kite = KiteConnect(api_key=self.api_key)
        self.access_token = None

    # Step 1 — Get login URL
    def get_login_url(self):
        return self.kite.login_url()

    # Step 2 — After Zerodha redirects back with request_token
    def generate_session(self, request_token):
        data = self.kite.generate_session(request_token, api_secret=self.api_secret)
        self.access_token = data["access_token"]
        self.kite.set_access_token(self.access_token)
        return {"status": "Login successful"}

    # Get available cash balance
    def get_balance(self):
        margins = self.kite.margins()
        return margins["equity"]["available"]["cash"]

    # Get current positions
    def get_positions(self):
        return self.kite.positions()

    # Place a market order
    def place_order(self, symbol, quantity, transaction_type):
        order_id = self.kite.place_order(
            variety=self.kite.VARIETY_REGULAR,
            exchange=self.kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            product=self.kite.PRODUCT_MIS,
            order_type=self.kite.ORDER_TYPE_MARKET
        )
        return order_id