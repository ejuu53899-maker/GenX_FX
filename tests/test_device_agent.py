import pytest
from agents.workers.genx_device_agent import GENXDeviceAgent
from agents.workers.mini_pc import MiniPCAgent
from agents.common.message_bus import MessageBus
from agents.common.schemas import Task, PermissionLevel


def test_device_agent_telemetry_and_commands():
    agent = GENXDeviceAgent()
    telemetry = agent.get_telemetry()
    assert telemetry["device"] == "BLUEDIM"
    assert telemetry["cpu"] == "N5105"
    assert telemetry["status"] == "online"

    # Command tests
    res_stop = agent.process_remote_command({"command": "stop_mt5"})
    assert res_stop["mt5"] == "stopped"

    res_start = agent.process_remote_command({"command": "start_trading"})
    assert res_start["mt5"] == "running"

    res_backup = agent.process_remote_command({"command": "backup_data"})
    assert res_backup["status"] == "BACKUP_COMPLETED"


@pytest.mark.asyncio
async def test_mini_pc_agent_device_integration():
    bus = MessageBus()
    mini_pc = MiniPCAgent(bus)

    task = Task(
        title="Get Telemetry",
        description="Fetch BLUEDIM device telemetry",
        assigned_agent="MiniPCWorker",
        required_level=PermissionLevel.LEVEL_1_ANALYZE,
        parameters={"action": "DEVICE_TELEMETRY"},
    )

    res_task = await mini_pc.execute_task(task)
    assert res_task.status == "COMPLETED"
    assert res_task.result["device"] == "BLUEDIM"
