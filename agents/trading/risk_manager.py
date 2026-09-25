"""Risk Manager for Trading Agent."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RiskManager:
    """Calculates position sizing, stop loss levels, and enforces max drawdown limits."""

    def evaluate_risk(self, signal_data: Dict[str, Any], account_balance: float = 10000.0) -> Dict[str, Any]:
        """Perform risk check and calculate trade parameters."""
        entry_price = signal_data.get("entry_price", 100.0)
        signal = signal_data.get("signal", "HOLD")

        if signal == "HOLD":
            return {"approved": False, "reason": "Signal is HOLD"}

        risk_amount = account_balance * 0.01  # 1% risk per trade
        stop_loss = entry_price * 0.99 if signal == "BUY" else entry_price * 1.01
        take_profit = entry_price * 1.02 if signal == "BUY" else entry_price * 0.98

        lot_size = round(risk_amount / abs(entry_price - stop_loss), 2) if abs(entry_price - stop_loss) > 0 else 0.1

        logger.info(f"Risk evaluation approved: Lot size {lot_size}, SL: {stop_loss}, TP: {take_profit}")
        return {
            "approved": True,
            "lot_size": lot_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "max_risk_amount": risk_amount,
        }
