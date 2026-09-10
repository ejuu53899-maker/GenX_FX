"""Decision Engine for Commander Agent."""

import logging
from typing import Dict, Any, Tuple
from agents.common.schemas import PermissionLevel

logger = logging.getLogger(__name__)


class DecisionEngine:
    """Answers 'Which agent should handle this?' and 'Is this action safe?'."""

    AGENT_ROLES: Dict[str, str] = {
        "code_generation": "Builder",
        "testing": "Builder",
        "git_commit": "Builder",
        "deployment": "DevOps",
        "container_management": "DevOps",
        "server_monitoring": "DevOps",
        "market_scanning": "Trading",
        "trade_execution": "Trading",
        "risk_assessment": "Trading",
        "security_check": "Guardian",
        "secret_management": "Guardian",
        "emergency_stop": "Guardian",
        "local_ai_inference": "MiniPCWorker",
        "dev_environment": "LaptopWorker",
        "skill_package_install": "USBIntelligenceWorker",
    }

    def route_task_to_agent(self, task_type: str) -> str:
        """Answer 'Which agent should handle this?'"""
        agent = self.AGENT_ROLES.get(task_type, "Commander")
        logger.info(f"Routed task type '{task_type}' to agent '{agent}'.")
        return agent

    def evaluate_safety(self, action: str, parameters: Dict[str, Any], agent_permission: PermissionLevel) -> Tuple[bool, str]:
        """Answer 'Is this action safe?'"""
        # Checks against critical operations
        if action == "EXECUTE_LIVE_TRADE":
            amount = parameters.get("amount", 0)
            if amount > 10000 and agent_permission < PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS:
                return False, "Live trade exceeds $10,000 threshold and requires LEVEL 5 permission"

        if action == "PURGE_DATABASE":
            return False, "Purging production database is an unsafe action"

        return True, "Action evaluated as safe"
