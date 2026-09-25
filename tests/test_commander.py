import pytest
from agents.common.message_bus import MessageBus
from agents.common.schemas import PermissionLevel, Task, SystemState
from agents.commander.commander_agent import CommanderAgent
from agents.commander.planner import StrategicPlanner
from agents.commander.decision_engine import DecisionEngine


def test_strategic_planner():
    planner = StrategicPlanner()
    tasks = planner.create_execution_plan("DEVELOP_FEATURE", {"feature_name": "AI_Trade_Signal"})
    assert len(tasks) == 3
    assert tasks[0].assigned_agent == "Builder"
    assert tasks[2].assigned_agent == "DevOps"


def test_decision_engine():
    de = DecisionEngine()
    assert de.route_task_to_agent("code_generation") == "Builder"
    assert de.route_task_to_agent("deployment") == "DevOps"
    assert de.route_task_to_agent("trade_execution") == "Trading"

    safe, reason = de.evaluate_safety("PURGE_DATABASE", {}, PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS)
    assert safe is False
    assert "unsafe" in reason.lower()


@pytest.mark.asyncio
async def test_commander_agent_dispatch():
    bus = MessageBus()
    commander = CommanderAgent(bus)

    dispatched = await commander.plan_and_dispatch_goal("DEVELOP_FEATURE", {"feature_name": "TestFeature"})
    assert len(dispatched) == 3
    assert commander.task_queue.size() == 3
