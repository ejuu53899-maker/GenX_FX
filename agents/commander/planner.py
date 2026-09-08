"""Planner for Commander Agent - Answers 'What should happen next?'."""

import logging
from typing import List, Dict, Any
from agents.common.schemas import Task, PermissionLevel

logger = logging.getLogger(__name__)


class StrategicPlanner:
    """Decomposes system goals into executable multi-agent task plans."""

    def create_execution_plan(self, goal: str, context: Dict[str, Any]) -> List[Task]:
        """Create a list of Tasks to accomplish the given goal."""
        tasks: List[Task] = []
        logger.info(f"StrategicPlanner creating plan for goal: '{goal}'")

        if goal == "DEVELOP_FEATURE":
            feature_name = context.get("feature_name", "new_feature")
            tasks.append(
                Task(
                    title=f"Generate Code for {feature_name}",
                    description=f"Create source code for {feature_name}",
                    assigned_agent="Builder",
                    required_level=PermissionLevel.LEVEL_2_CREATE_FILES,
                    parameters={"action": "GENERATE_CODE", "feature": feature_name},
                )
            )
            tasks.append(
                Task(
                    title=f"Run Tests for {feature_name}",
                    description=f"Verify unit tests pass for {feature_name}",
                    assigned_agent="Builder",
                    required_level=PermissionLevel.LEVEL_2_CREATE_FILES,
                    parameters={"action": "RUN_TESTS", "feature": feature_name},
                )
            )
            tasks.append(
                Task(
                    title=f"Deploy {feature_name}",
                    description=f"Deploy verified code for {feature_name}",
                    assigned_agent="DevOps",
                    required_level=PermissionLevel.LEVEL_3_DEPLOY,
                    parameters={"action": "DEPLOY", "feature": feature_name},
                )
            )

        elif goal == "ANALYZE_AND_TRADE":
            symbol = context.get("symbol", "BTC/USD")
            tasks.append(
                Task(
                    title=f"Scan Market Data for {symbol}",
                    description=f"Fetch latest indicators and order book for {symbol}",
                    assigned_agent="Trading",
                    required_level=PermissionLevel.LEVEL_1_ANALYZE,
                    parameters={"action": "SCAN_MARKET", "symbol": symbol},
                )
            )
            tasks.append(
                Task(
                    title=f"Evaluate Risk for {symbol}",
                    description=f"Calculate position sizing and stop loss for {symbol}",
                    assigned_agent="Trading",
                    required_level=PermissionLevel.LEVEL_1_ANALYZE,
                    parameters={"action": "EVALUATE_RISK", "symbol": symbol},
                )
            )

        else:
            # Default generic task
            tasks.append(
                Task(
                    title=f"Execute Goal: {goal}",
                    description=f"Process general goal: {goal}",
                    assigned_agent="Commander",
                    required_level=PermissionLevel.LEVEL_1_ANALYZE,
                    parameters={"goal": goal},
                )
            )

        return tasks
