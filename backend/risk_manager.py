from datetime import datetime, time

class RiskManager:
    def __init__(self, max_capital=500):
        self.max_capital = max_capital

    def market_open(self):
        now = datetime.now().time()
        return time(9,15) <= now <= time(15,15)
