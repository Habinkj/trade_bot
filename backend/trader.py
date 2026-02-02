from backend.risk_manager import RiskManager
from backend.api import BrokerAPI  # Your Zerodha/Kite wrapper
from backend.strategy import Strategy


class Trader:
    def __init__(self, config):
        self.api = BrokerAPI(config)
        self.strategy = Strategy()
        self.risk = RiskManager(
            max_capital=config["max_capital"],
            max_risk_per_trade=config["risk_per_trade"],
            max_trades_per_day=config["max_trades_per_day"]
        )

    # ================= MAIN BOT LOOP =================
    def run(self):
        print("🚀 Trader started...")

        if not self.risk.market_open():
            print("⛔ Market closed")
            return

        balance = self.api.get_available_cash()
        print(f"💰 Available cash: {balance}")

        symbols = self.api.get_watchlist()

        for symbol in symbols:
            signal = self.strategy.check_signal(symbol)

            if signal == "BUY":
                self.execute_trade(symbol, "BUY", balance)

            elif signal == "SELL":
                self.execute_trade(symbol, "SELL", balance)

    # ================= TRADE EXECUTION =================
    def execute_trade(self, symbol, side, balance):
        can_trade, reason = self.risk.can_take_trade()
        if not can_trade:
            print(f"❌ Trade blocked: {reason}")
            return

        price = self.api.get_ltp(symbol)
        qty, reason = self.risk.calculate_position_size(balance, price)

        if qty <= 0:
            print(f"❌ Position sizing failed: {reason}")
            return

        order_id = self.api.place_order(symbol, side, qty)

        if order_id:
            print(f"✅ {side} Order placed for {symbol} | Qty: {qty} | Price: {price}")
        else:
            print("❌ Order failed")