"""
GENX Trading Intelligence Handler v3.6.9
Orchestrates trading signal pipeline:
Market Data -> Analysis Agent -> Strategy Agent -> Risk Gatekeeper -> Dynamic Approval -> MT5 EA Execution Bridge
"""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from src.agents.identity import PermissionLevel
from src.security.gatekeeper import SecurityGatekeeper

logger = logging.getLogger(__name__)


class TradeSignal(BaseModel):
    symbol: str
    action: str  # BUY, SELL, CLOSE
    confidence: float
    position_size_pct: float = 0.5
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    timeframe: str = "H1"


class TradingIntelligenceHandler:
    """
    Connects Trading AI signals with Risk Gatekeeper and MetaTrader 5 EA Bridge.
    """

    def __init__(self, gatekeeper: SecurityGatekeeper):
        self.gatekeeper = gatekeeper

    def process_trade_signal(
        self,
        signal: TradeSignal,
        agent_id: str = "GENX-TRADER-001",
        agent_permission: PermissionLevel = PermissionLevel.LEVEL_3_APPROVAL,
        human_approved: bool = False,
        daily_drawdown_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        Processes trade signal through Risk Check, Approval Gate, and EA Execution Bridge.
        """
        logger.info(f"Processing trade signal for {signal.symbol} ({signal.action}, conf: {signal.confidence})")

        # Required permission to execute trade is Level 3 (Execute with approval) or Level 4
        required_permission = PermissionLevel.LEVEL_3_APPROVAL

        context = {
            "symbol": signal.symbol,
            "action": signal.action,
            "confidence": signal.confidence,
            "position_size_pct": signal.position_size_pct,
            "daily_drawdown_pct": daily_drawdown_pct,
            "human_approved": human_approved
        }

        # Gatekeeper evaluation
        permitted = self.gatekeeper.evaluate_permission(
            agent_id=agent_id,
            agent_permission=agent_permission,
            required_permission=required_permission,
            action="execute_trade",
            context=context
        )

        if not permitted:
            return {
                "status": "rejected",
                "reason": "Security/Risk gatekeeper rejected execution.",
                "signal": signal.model_dump()
            }

        # Simulate MT5 EA Bridge dispatch
        execution_response = {
            "status": "executed",
            "broker": "MT5 Terminal",
            "symbol": signal.symbol,
            "action": signal.action,
            "executed_price": 2035.50 if signal.symbol == "XAUUSD" else 1.0850,
            "ticket_id": 982341,
            "agent_id": agent_id
        }

        logger.info(f"Successfully executed trade on MT5: {execution_response}")
        return execution_response
