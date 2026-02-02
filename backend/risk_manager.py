from datetime import datetime, time


class RiskManager:
    def __init__(self, max_capital=500, max_risk_per_trade=0.20, max_trades_per_day=5):
        """
        max_capital: total capital allowed for the bot
        max_risk_per_trade: % of capital allowed per trade (0.20 = 20%)
        max_trades_per_day: stop bot after too many trades
        """
        self.max_capital = max_capital
        self.max_risk_per_trade = max_risk_per_trade
        self.max_trades_per_day = max_trades_per_day
        self.trades_taken_today = 0

    # ================= MARKET TIME CONTROL =================
    def market_open(self):
        now = datetime.now().time()
        return time(9, 15) <= now <= time(15, 15)

    # ================= CAPITAL PROTECTION =================
    def calculate_position_size(self, available_cash, price_per_stock):
        """
        Decide how many shares we can buy safely
        """
        if available_cash <= 0:
            return 0, "No cash available"

        allowed_trade_value = available_cash * self.max_risk_per_trade
        quantity = int(allowed_trade_value // price_per_stock)

        if quantity <= 0:
            return 0, "Stock too expensive for current risk settings"

        return quantity, "OK"

    # ================= DAILY TRADE LIMIT =================
    def can_take_trade(self):
        if self.trades_taken_today >= self.max_trades_per_day:
            return False, "Daily trade limit reached"

        self.trades_taken_today += 1
        return True, "Trade allowed"

    # ================= LOSS PROTECTION (OPTIONAL FUTURE) =================
    def capital_within_limit(self, total_invested):
        """
        Prevents bot from exceeding total allowed capital
        """
        return total_invested <= self.max_capital