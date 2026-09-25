import pytest
import asyncio
from agents.common.schemas import PermissionLevel, AgentMessage, Task, Skill
from agents.common.permissions import PermissionManager
from agents.common.message_bus import MessageBus
from agents.common.base_agent import BaseAgent


def test_permission_levels():
    pm = PermissionManager()
    assert pm.get_agent_permission("Commander") == PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS
    assert pm.get_agent_permission("Builder") == PermissionLevel.LEVEL_2_CREATE_FILES
    assert pm.has_permission("Builder", PermissionLevel.LEVEL_2_CREATE_FILES)
    assert not pm.has_permission("Builder", PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS)


@pytest.mark.asyncio
async def test_message_bus_pub_sub():
    pm = PermissionManager()
    bus = MessageBus(permission_manager=pm)
    received = []

    def handler(msg: AgentMessage):
        received.append(msg)

    bus.subscribe("test.topic", handler)

    msg = AgentMessage(
        sender="Commander",
        receiver="ALL",
        topic="test.topic",
        payload={"hello": "world"},
        level_required=PermissionLevel.LEVEL_1_ANALYZE,
    )
    success = await bus.publish(msg)
    assert success is True
    assert len(received) == 1
    assert received[0].payload["hello"] == "world"


@pytest.mark.asyncio
async def test_base_agent_execution():
    bus = MessageBus()
    agent = BaseAgent(
        name="TestAgent",
        role="Tester",
        default_permission=PermissionLevel.LEVEL_3_DEPLOY,
        message_bus=bus,
    )

    task = Task(
        title="Test Task",
        description="A sample test task",
        assigned_agent="TestAgent",
        required_level=PermissionLevel.LEVEL_2_CREATE_FILES,
    )

    res_task = await agent.execute_task(task)
    assert res_task.status == "COMPLETED"
    assert len(agent.experiences) == 1
    assert agent.experiences[0].status == "SUCCESS"
