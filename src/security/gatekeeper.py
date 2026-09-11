"""
GENX Security Gatekeeper & Audit Layer (v3.6.9)
Controls agent permission levels (0 to 4), dynamic trade risk gating, credential vault access, and audit logging.
"""

import time
import logging
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from src.agents.identity import PermissionLevel

logger = logging.getLogger(__name__)


class AuditLogEntry(BaseModel):
    timestamp: float = Field(default_factory=time.time)
    agent_id: str
    action: str
    permission_required: PermissionLevel
    permission_granted: PermissionLevel
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)


class SecurityGatekeeper:
    """
    Security Gatekeeper enforcing Level 0-4 permission boundaries, dynamic trade risk rules, and audit logging.
    """

    def __init__(self, max_position_size_pct: float = 1.0, max_daily_drawdown_pct: float = 2.0):
        self.max_position_size_pct = max_position_size_pct
        self.max_daily_drawdown_pct = max_daily_drawdown_pct
        self.audit_trail: List[AuditLogEntry] = []

    def evaluate_permission(
        self,
        agent_id: str,
        agent_permission: PermissionLevel,
        required_permission: PermissionLevel,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Evaluates whether an agent has sufficient permission level to perform an action.
        """
        context = context or {}
        granted = agent_permission >= required_permission

        # Dynamic risk check for trade execution
        if granted and action == "execute_trade":
            position_size_pct = context.get("position_size_pct", 0.5)
            daily_drawdown_pct = context.get("daily_drawdown_pct", 0.0)

            # Rule: If position size > max allowed or drawdown exceeds threshold, require human approval (Level 3)
            if position_size_pct > self.max_position_size_pct or daily_drawdown_pct >= self.max_daily_drawdown_pct:
                if agent_permission < PermissionLevel.LEVEL_3_APPROVAL or not context.get("human_approved", False):
                    granted = False
                    logger.warning(
                        f"Trade execution blocked by risk gate for agent {agent_id}. "
                        f"Pos Size: {position_size_pct}%, Drawdown: {daily_drawdown_pct}%"
                    )

        entry = AuditLogEntry(
            agent_id=agent_id,
            action=action,
            permission_required=required_permission,
            permission_granted=agent_permission,
            status="ALLOWED" if granted else "DENIED",
            details=context
        )
        self.audit_trail.append(entry)
        return granted

    def get_audit_trail(self, limit: int = 50) -> List[AuditLogEntry]:
        return self.audit_trail[-limit:]
