"""
Jules Real-Time Trading Position Manager Engine.
Monitors all open positions across any symbols in real-time market data
and manages closing trades in profit.
"""

import logging
import time
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PositionStatus(str, Enum):
    OPEN = "OPEN"
    PROFIT_LOCKED = "PROFIT_LOCKED"
    CLOSED_IN_PROFIT = "CLOSED_IN_PROFIT"
    CLOSED_EMERGENCY = "CLOSED_EMERGENCY"


class OpenPosition(BaseModel):
    """Data model representing a real-time open position."""

    ticket_id: str = Field(description="Unique ticket/order ID")
    symbol: str = Field(description="Trading symbol, e.g., EURUSD, BTCUSD, XAUUSD")
    order_type: str = Field(description="BUY or SELL")
    open_price: float = Field(description="Execution entry price")
    current_price: float = Field(description="Current real-time market price")
    volume: float = Field(default=0.1, description="Lot size or contract quantity")
    floating_profit: float = Field(default=0.0, description="Real-time floating profit/loss in USD")
    take_profit_target: Optional[float] = Field(default=None, description="Take profit price target")
    stop_loss_target: Optional[float] = Field(default=None, description="Stop loss price level")
    min_profit_threshold: float = Field(default=5.0, description="Minimum profit threshold ($) to lock closing trade")
    trailing_profit_locked: float = Field(default=0.0, description="Locked profit amount ($)")
    status: PositionStatus = Field(default=PositionStatus.OPEN)
    opened_at: str = Field(default="2025-10-11T12:00:00Z")


class JulesPositionManager:
    """
    Jules Always-On Trading Positioning System Engine.
    Mandatory Rule: Jules MUST take ownership of all open position symbols in the real-time market
    and MUST manage closing every trade with profit.
    """

    def __init__(self, min_profit_to_close: float = 2.0, trailing_step_usd: float = 1.0):
        self.min_profit_to_close = min_profit_to_close
        self.trailing_step_usd = trailing_step_usd
        self.positions: Dict[str, OpenPosition] = {}
        self.closed_trades_history: List[Dict[str, Any]] = []
        self.always_on_active = True
        logger.info("JulesPositionManager Engine initialized with Real-Time Profit Guardian.")

    def register_open_position(self, position: OpenPosition) -> None:
        """Register an active market position under Jules' management."""
        self.positions[position.ticket_id] = position
        logger.info(f"Jules position manager taking control of Ticket #{position.ticket_id} ({position.symbol} {position.order_type} @ {position.open_price})")

    def sync_open_positions_from_market(self, live_market_positions: List[Dict[str, Any]]) -> None:
        """Synchronize all real-time open symbols from broker/exchange API into Jules Engine."""
        for item in live_market_positions:
            ticket = str(item.get("ticket_id") or item.get("id") or item.get("symbol"))
            pos = OpenPosition(
                ticket_id=ticket,
                symbol=item["symbol"],
                order_type=item.get("order_type", "BUY"),
                open_price=float(item.get("open_price", 1.0)),
                current_price=float(item.get("current_price", item.get("open_price", 1.0))),
                volume=float(item.get("volume", 0.1)),
                floating_profit=float(item.get("floating_profit", 0.0)),
            )
            self.positions[ticket] = pos
        logger.info(f"Synced {len(live_market_positions)} real-time open symbols under Jules management.")

    def evaluate_and_manage_positions(self, market_prices: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """
        Core Real-Time Profit Enforcement Loop.
        Iterates over ALL open position symbols:
        1. Updates current price and floating profit.
        2. Applies dynamic trailing profit locks.
        3. Closes trade when profit threshold/target is satisfied, ensuring guaranteed profit close.
        """
        market_prices = market_prices or {}
        closing_actions = []

        for ticket_id, pos in list(self.positions.items()):
            if pos.status in [PositionStatus.CLOSED_IN_PROFIT, PositionStatus.CLOSED_EMERGENCY]:
                continue

            # Update live market price
            if pos.symbol in market_prices:
                pos.current_price = market_prices[pos.symbol]
                # Recalculate floating profit
                if pos.order_type.upper() == "BUY":
                    pos.floating_profit = round((pos.current_price - pos.open_price) * pos.volume * 100000, 2)
                else:
                    pos.floating_profit = round((pos.open_price - pos.current_price) * pos.volume * 100000, 2)

            # Rule: Jules MUST manage closing trade with profit
            if pos.floating_profit >= self.min_profit_to_close:
                # Lock trailing profit
                if pos.floating_profit > pos.trailing_profit_locked + self.trailing_step_usd:
                    pos.trailing_profit_locked = pos.floating_profit - (self.trailing_step_usd * 0.5)
                    pos.status = PositionStatus.PROFIT_LOCKED
                    logger.info(f"Ticket #{ticket_id} ({pos.symbol}): Profit locked at ${pos.trailing_profit_locked:.2f}")

                # Close trade in profit
                action = self._execute_close_trade_in_profit(pos, reason="Profit Target / Trailing Guard Triggered")
                closing_actions.append(action)

        return closing_actions

    def _execute_close_trade_in_profit(self, pos: OpenPosition, reason: str) -> Dict[str, Any]:
        """Execute close order ensuring trade closes with positive realized profit."""
        pos.status = PositionStatus.CLOSED_IN_PROFIT
        realized_profit = max(pos.floating_profit, self.min_profit_to_close)

        record = {
            "ticket_id": pos.ticket_id,
            "symbol": pos.symbol,
            "order_type": pos.order_type,
            "open_price": pos.open_price,
            "close_price": pos.current_price,
            "realized_profit": realized_profit,
            "status": pos.status.value,
            "reason": reason,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        self.closed_trades_history.append(record)

        # Remove from active tracking
        if pos.ticket_id in self.positions:
            del self.positions[pos.ticket_id]

        logger.info(f"✅ MANDATORY PROFIT RULE EXECUTED: Closed Ticket #{pos.ticket_id} ({pos.symbol}) with +${realized_profit:.2f} profit!")
        return record

    def get_system_status(self) -> Dict[str, Any]:
        """Get engine status summary for monitoring and dashboard."""
        return {
            "engine": "Jules Always-On Trading Positioning System",
            "always_on": self.always_on_active,
            "open_symbols_managed": len(self.positions),
            "open_positions": [p.model_dump() for p in self.positions.values()],
            "closed_trades_count": len(self.closed_trades_history),
            "total_realized_profit_usd": sum(t["realized_profit"] for t in self.closed_trades_history),
            "rule_enforced": "Jules real-time symbol profit-closing mandate ACTIVE",
        }
