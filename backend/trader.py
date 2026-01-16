import logging
from dhanhq import dhanhq

logger = logging.getLogger(__name__)

class DhanTrader:
    def __init__(self, client_id, access_token, dry_run=True):
        self.dhan = dhanhq(client_id, access_token)
        self.dry_run = dry_run

    def place_buy_order(self, security_id, quantity, price):
        if self.dry_run:
            logger.info(f"[DRY RUN] BUY {security_id}")
            return True, "DRY_RUN"

        response = self.dhan.place_order(
            security_id=security_id,
            exchange_segment=dhanhq.NSE,
            transaction_type=dhanhq.BUY,
            quantity=quantity,
            order_type=dhanhq.MARKET,
            product_type=dhanhq.INTRA,
            validity=dhanhq.DAY
        )
        return True, response
