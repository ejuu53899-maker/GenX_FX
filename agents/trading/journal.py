"""Trade Journal for Trading Agent."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class TradeJournal:
    """Logs trade records and performance history for AI learning loop."""

    def __init__(self):
        self._journal_entries: List[Dict[str, Any]] = []

    def log_trade(self, order_result: Dict[str, Any], risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record executed trade in journal."""
        entry = {
            "order_id": order_result.get("order_id"),
            "symbol": order_result.get("symbol"),
            "lot_size": order_result.get("lot_size"),
            "executed_price": order_result.get("executed_price"),
            "status": order_result.get("status"),
            "risk_parameters": risk_data,
        }
        self._journal_entries.append(entry)
        logger.info(f"Trade journal entry recorded for {order_result.get('order_id')}")
        return entry

    def get_entries(self) -> List[Dict[str, Any]]:
        """Return journal entries."""
        return list(self._journal_entries)
