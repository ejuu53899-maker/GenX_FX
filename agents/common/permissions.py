"""Permission management system for GENX agents."""

import logging
from typing import Dict, Optional
from .schemas import PermissionLevel

logger = logging.getLogger(__name__)


class PermissionManager:
    """Manages and validates agent permission levels."""

    DEFAULT_AGENT_PERMISSIONS: Dict[str, PermissionLevel] = {
        "Commander": PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
        "Guardian": PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
        "Security": PermissionLevel.LEVEL_4_EXECUTE_ACTIONS,
        "Builder": PermissionLevel.LEVEL_2_CREATE_FILES,
        "DevOps": PermissionLevel.LEVEL_3_DEPLOY,
        "Trading": PermissionLevel.LEVEL_1_ANALYZE,  # Default analyze, upgraded to LEVEL 5 for approved trade executions
        "Market": PermissionLevel.LEVEL_1_ANALYZE,
        "MiniPCWorker": PermissionLevel.LEVEL_2_CREATE_FILES,
        "LaptopWorker": PermissionLevel.LEVEL_3_DEPLOY,
        "USBIntelligenceWorker": PermissionLevel.LEVEL_2_CREATE_FILES,
    }

    def __init__(self, custom_permissions: Optional[Dict[str, PermissionLevel]] = None):
        self._permissions: Dict[str, PermissionLevel] = dict(self.DEFAULT_AGENT_PERMISSIONS)
        if custom_permissions:
            self._permissions.update(custom_permissions)

    def register_agent_permission(self, agent_name: str, level: PermissionLevel) -> None:
        """Register or update permission level for an agent."""
        self._permissions[agent_name] = level
        logger.info(f"Registered agent '{agent_name}' with permission level {level.name} ({level.value})")

    def get_agent_permission(self, agent_name: str) -> PermissionLevel:
        """Get assigned permission level for an agent."""
        return self._permissions.get(agent_name, PermissionLevel.LEVEL_0_READ_ONLY)

    def has_permission(self, agent_name: str, required_level: PermissionLevel) -> bool:
        """Check if an agent has the required permission level."""
        agent_level = self.get_agent_permission(agent_name)
        allowed = agent_level >= required_level
        if not allowed:
            logger.warning(
                f"Permission denied for '{agent_name}': holds {agent_level.name} ({agent_level.value}), "
                f"required {required_level.name} ({required_level.value})"
            )
        return allowed

    def authorize_action(self, agent_name: str, required_level: PermissionLevel, action_name: str) -> bool:
        """Authorize an explicit action or raise error/return false if denied."""
        if self.has_permission(agent_name, required_level):
            logger.info(f"Action '{action_name}' authorized for '{agent_name}'.")
            return True
        else:
            logger.error(f"Action '{action_name}' DENIED for '{agent_name}'.")
            return False
