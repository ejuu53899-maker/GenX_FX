import pytest
from agents.common.message_bus import MessageBus
from agents.common.schemas import PermissionLevel, Task
from agents.trading.trading_agent import TradingAgent
from agents.builder.builder_agent import BuilderAgent
from agents.devops.devops_agent import DevOpsAgent


@pytest.mark.asyncio
async def test_trading_agent_pipeline():
    bus = MessageBus()
    trading = TradingAgent(bus)

    # Without level 5, execution status should require approval or signal only
    res = await trading.execute_trade_pipeline("BTC/USD")
    assert res["status"] in ["APPROVAL_REQUIRED", "SKIPPED"]

    # Upgrade permission to Level 5 Financial Operations
    bus.permission_manager.register_agent_permission("Trading", PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS)
    res_executed = await trading.execute_trade_pipeline("BTC/USD")
    assert res_executed["status"] == "EXECUTED"
    assert "order" in res_executed
    assert res_executed["order"]["executed_price"] > 0


@pytest.mark.asyncio
async def test_builder_agent_tasks():
    bus = MessageBus()
    builder = BuilderAgent(bus)

    gen_task = Task(
        title="Generate Class",
        description="Gen code",
        assigned_agent="Builder",
        required_level=PermissionLevel.LEVEL_2_CREATE_FILES,
        parameters={"action": "GENERATE_CODE", "class_name": "TestClass", "methods": ["run"]},
    )
    res_task = await builder.execute_task(gen_task)
    assert res_task.status == "COMPLETED"
    assert "class TestClass" in res_task.result["code"]


@pytest.mark.asyncio
async def test_devops_agent_tasks():
    bus = MessageBus()
    devops = DevOpsAgent(bus)

    deploy_task = Task(
        title="Deploy Service",
        description="Deploy app",
        assigned_agent="DevOps",
        required_level=PermissionLevel.LEVEL_3_DEPLOY,
        parameters={"action": "DEPLOY", "service": "TradingBridge", "version": "1.2.0"},
    )
    res_task = await devops.execute_task(deploy_task)
    assert res_task.status == "COMPLETED"
    assert res_task.result["status"] == "DEPLOYED"
