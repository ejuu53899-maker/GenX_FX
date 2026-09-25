"""Trading Intelligence Agent - Financial Analysis Worker."""

import logging
from typing import Dict, Any
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task
from agents.common.message_bus import MessageBus

from .market_scanner import MarketScanner
from .strategy_engine import StrategyEngine
from .risk_manager import RiskManager
from .execution_bridge import ExecutionBridge
from .journal import TradeJournal

logger = logging.getLogger(__name__)


class TradingAgent(BaseAgent):
    """Trading Intelligence Agent running market scanning, strategy evaluation, risk check, execution, and trade journaling."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="Trading",
            role="Financial Analysis Worker",
            default_permission=PermissionLevel.LEVEL_1_ANALYZE,
            message_bus=message_bus,
        )
        self.market_scanner = MarketScanner()
        self.strategy_engine = StrategyEngine()
        self.risk_manager = RiskManager()
        self.execution_bridge = ExecutionBridge()
        self.journal = TradeJournal()

    async def execute_trade_pipeline(self, symbol: str) -> Dict[str, Any]:
        """Runs decision flow: Market Data -> Analysis -> Strategy -> Risk Check -> Execution -> Trade Journal -> Learning."""
        # 1. Market Data
        market_data = self.market_scanner.scan_symbol(symbol)

        # 2. Strategy
        signal_data = self.strategy_engine.evaluate_signal(market_data)

        # 3. Risk Check
        risk_check = self.risk_manager.evaluate_risk(signal_data)

        if not risk_check.get("approved"):
            return {
                "status": "SKIPPED",
                "reason": risk_check.get("reason", "Risk check failed"),
                "signal": signal_data,
            }

        # 4. Permission check for trade execution
        if not self.check_permission(PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS):
            logger.warning("Trading Agent lacks LEVEL 5 permission for live execution. Generating signal only.")
            return {
                "status": "APPROVAL_REQUIRED",
                "reason": "Execution requires Level 5 Financial Operations permission",
                "signal": signal_data,
                "risk_parameters": risk_check,
            }

        # 5. Execution
        order_res = self.execution_bridge.execute_order(
            symbol=symbol,
            order_type=signal_data["signal"],
            lot_size=risk_check["lot_size"],
            price=market_data["price"],
        )

        # 6. Trade Journal
        journal_entry = self.journal.log_trade(order_res, risk_check)

        # 7. Learning Loop Experience Recording
        self.record_experience(
            action=f"Trade Pipeline for {symbol}",
            result=order_res,
            status="SUCCESS",
            analysis=f"Executed {signal_data['signal']} order on {symbol}",
            improvement_plan="Monitor drawdown and profit target hit rate",
        )

        return {
            "status": "EXECUTED",
            "order": order_res,
            "journal_entry": journal_entry,
        }

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Process Trading Agent tasks."""
        action = task.parameters.get("action")
        symbol = task.parameters.get("symbol", "BTC/USD")

        if action == "SCAN_MARKET":
            return self.market_scanner.scan_symbol(symbol)

        elif action == "EVALUATE_STRATEGY":
            mdata = self.market_scanner.scan_symbol(symbol)
            return self.strategy_engine.evaluate_signal(mdata)

        elif action == "EXECUTE_PIPELINE":
            return await self.execute_trade_pipeline(symbol)

        return {"status": "COMPLETED", "message": f"Trading agent processed task '{task.title}'"}
