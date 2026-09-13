"""
Unit tests for GENX Security Gatekeeper.
"""

import pytest
from src.agents.identity import PermissionLevel
from src.security.gatekeeper import SecurityGatekeeper


def test_security_permission_evaluation():
    gatekeeper = SecurityGatekeeper(max_position_size_pct=1.0, max_daily_drawdown_pct=2.0)

    # Permission check: Level 1 agent trying Level 3 action -> Denied
    allowed = gatekeeper.evaluate_permission(
        agent_id="GENX-ANALYST",
        agent_permission=PermissionLevel.LEVEL_1_ANALYZE,
        required_permission=PermissionLevel.LEVEL_3_APPROVAL,
        action="execute_trade"
    )
    assert not allowed

    # Trade Risk Gate: Position size > max (2.5% > 1.0%) without human approval -> Denied
    allowed_risk = gatekeeper.evaluate_permission(
        agent_id="GENX-TRADER-001",
        agent_permission=PermissionLevel.LEVEL_3_APPROVAL,
        required_permission=PermissionLevel.LEVEL_3_APPROVAL,
        action="execute_trade",
        context={"position_size_pct": 2.5, "daily_drawdown_pct": 0.5, "human_approved": False}
    )
    assert not allowed_risk

    # Trade Risk Gate: Position size > max WITH human approval -> Allowed
    allowed_approved = gatekeeper.evaluate_permission(
        agent_id="GENX-TRADER-001",
        agent_permission=PermissionLevel.LEVEL_3_APPROVAL,
        required_permission=PermissionLevel.LEVEL_3_APPROVAL,
        action="execute_trade",
        context={"position_size_pct": 2.5, "daily_drawdown_pct": 0.5, "human_approved": True}
    )
    assert allowed_approved
