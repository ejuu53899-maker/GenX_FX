import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RiskManager:
    """Manages trading risk, including position sizing and stop-loss logic"""

    def __init__(self, max_risk_per_trade: float = 0.02, default_stop_loss_pct: float = 0.05):
        self.max_risk_per_trade = max_risk_per_trade
        self.default_stop_loss_pct = default_stop_loss_pct

    def calculate_position_size(self, balance: float, risk_per_trade: float = None) -> float:
        """Calculate the trade size based on the risk percentage"""
        risk = risk_per_trade if risk_per_trade is not None else self.max_risk_per_trade
        return balance * risk

    def get_stop_loss_price(self, entry_price: float, side: str, stop_loss_pct: float = None) -> float:
        """Calculate the stop-loss price for a given entry price and side"""
        sl_pct = stop_loss_pct if stop_loss_pct is not None else self.default_stop_loss_pct

        if side.lower() == 'buy':
            return entry_price * (1 - sl_pct)
        elif side.lower() == 'sell':
            return entry_price * (1 + sl_pct)
        else:
            logger.error(f"Invalid side: {side}")
            return entry_price

    def check_trade_validity(self, trade_params: Dict[str, Any], current_balance: float = None) -> bool:
        """Validate if the trade parameters are within acceptable risk limits"""
        logger.info(f"Validating trade: {trade_params}")

        if current_balance is not None:
            trade_value = trade_params.get('price', 0) * trade_params.get('quantity', 0)
            if trade_value > current_balance:
                logger.warning(f"Insufficient balance: {current_balance} < {trade_value}")
                return False

        # Additional safety checks
        if trade_params.get('price', 0) <= 0:
            logger.warning("Invalid trade price")
            return False

        return True
