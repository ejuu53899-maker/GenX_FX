"""Access control manager for Guardian Agent."""

import logging
from typing import Dict
from agents.common.schemas import PermissionLevel

logger = logging.getLogger(__name__)


class AccessControlManager:
    """Controls access policies and verifies agent privilege boundaries."""

    def __init__(self):
        self._restricted_actions = {
            "EXECUTE_TRADE": PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
            "CHANGE_RISK_LIMITS": PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
            "DEPLOY_PRODUCTION": PermissionLevel.LEVEL_3_DEPLOY,
            "SYSTEM_RESTART": PermissionLevel.LEVEL_4_EXECUTE_ACTIONS,
            "EMERGENCY_STOP": PermissionLevel.LEVEL_4_EXECUTE_ACTIONS,
        }

    def verify_action_access(self, agent_name: str, agent_level: PermissionLevel, action: str) -> bool:
        """Verify if an agent is authorized for a specific restricted action."""
        required = self._restricted_actions.get(action, PermissionLevel.LEVEL_1_ANALYZE)
        if agent_level >= required:
            logger.info(f"Access granted to '{agent_name}' for action '{action}'.")
            return True
        logger.warning(
            f"Access DENIED to '{agent_name}' for action '{action}'. "
            f"Has {agent_level.name}, required {required.name}."
        )
        return False
