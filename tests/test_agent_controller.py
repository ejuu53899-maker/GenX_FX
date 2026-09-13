"""
Unit tests for GENX AI Agent Controller (Router, Dispatcher, Orchestrator).
"""

import pytest
from src.agents.identity import AgentIdentity, AgentCard, PermissionLevel, AgentStatus
from src.core.agent_controller.router import AgentRouter, RoutingPattern
from src.core.agent_controller.dispatcher import AgentDispatcher
from src.core.agent_controller.orchestrator import AgentCenterHandlerController


def test_agent_router_intent_detection():
    router = AgentRouter()
    assert router.detect_intent("Analyze XAUUSD market") == "market_analysis"
    assert router.detect_intent("Refactor python code") == "coding_task"
    assert router.detect_intent("Check MiniPC CPU usage") == "device_management"
    assert router.detect_intent("Start GENX Trading mission") == "mission_execution"


def test_agent_router_pattern_selection():
    router = AgentRouter()
    assert router.select_pattern("market_analysis", high_risk=False) == RoutingPattern.SPECIALIST
    assert router.select_pattern("mission_execution", high_risk=False) == RoutingPattern.HIERARCHICAL
    assert router.select_pattern("market_analysis", high_risk=True) == RoutingPattern.CONSENSUS


def test_agent_dispatcher_execution():
    router = AgentRouter()
    card = AgentCard(
        identity=AgentIdentity(
            agent_id="TEST-AGENT-01",
            name="Test Agent",
            role="Tester",
            status=AgentStatus.ACTIVE
        ),
        supported_intents=["market_analysis"]
    )
    router.register_agent(card)
    dispatcher = AgentDispatcher(router)

    route_info = router.route_request("Analyze market")
    result = dispatcher.dispatch(route_info)
    assert result["status"] == "success"


def test_orchestrator_process_command():
    controller = AgentCenterHandlerController()
    res = controller.process_command("Analyze XAUUSD market")
    assert res["dispatch"]["status"] == "success"
    assert "telemetry" in res
