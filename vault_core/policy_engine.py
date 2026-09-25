"""Policy Engine for GENX Vault - Validates Agent Permissions."""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class VaultPolicyEngine:
    """Enforces agent-specific secret access rules."""

    AGENT_PERMISSIONS: Dict[str, List[str]] = {
        "jules": ["read_templates", "request_access", "create_tasks", "audit", "read_dev_env"],
        "cursor": ["read_dev_env", "generate_code", "run_tests"],
        "warp": ["execute_commands", "restart_services"],
        "copilot": ["read_public_status"],
        "commander": ["read_dev_env", "read_templates", "request_access", "audit"],
        "guardian": ["read_dev_env", "read_prod_env", "request_access", "audit", "revoke_access"],
        "exnessvps": ["read_dev_env", "read_prod_env"],
    }

    def check_permission(self, agent_name: str, requested_action: str) -> bool:
        """Verify if agent is allowed to perform requested secret action."""
        allowed_actions = self.AGENT_PERMISSIONS.get(agent_name.lower(), [])
        if requested_action in allowed_actions or "all" in allowed_actions:
            logger.info(f"Vault Policy ALLOWED: '{agent_name}' -> '{requested_action}'")
            return True
        logger.warning(f"Vault Policy DENIED: '{agent_name}' -> '{requested_action}'")
        return False
