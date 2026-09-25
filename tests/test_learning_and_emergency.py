import pytest
from pathlib import Path
from agents.common.schemas import Experience, Skill, PermissionLevel, SystemState
from agents.common.learning_loop import LearningLoopManager
from agents.orchestrator import AgentOSOrchestrator


def test_learning_loop_logging_and_evolution(tmp_path: Path):
    llm = LearningLoopManager(data_dir=tmp_path)

    success_exp = Experience(
        agent_name="Trading",
        action="SCAN_MARKET",
        result={"price": 2350.5},
        status="SUCCESS",
        analysis="Market scan successful",
    )
    llm.log_experience(success_exp)
    assert (tmp_path / "memories" / f"memory_{success_exp.exp_id}.json").exists()

    fail_exp = Experience(
        agent_name="Trading",
        action="EXECUTE_ORDER",
        result={"error": "Slippage tolerance exceeded"},
        status="FAILURE",
        analysis="High volatility caused slippage breach",
    )
    llm.log_experience(fail_exp)
    assert (tmp_path / "failures" / f"failure_{fail_exp.exp_id}.json").exists()

    imp_plan = llm.generate_improvement_plan(fail_exp.exp_id)
    assert imp_plan is not None
    assert (tmp_path / "improvements" / f"improvement_{fail_exp.exp_id}.json").exists()

    base_skill = Skill(
        skill_id="SKILL-ORDER-01",
        name="OrderExecutionEngine",
        version="1.0.0",
        description="Base order execution engine",
    )
    evolved = llm.evolve_skill(base_skill, "1.0.1", "Dynamic slippage adjustment")
    assert evolved.version == "1.0.1"
    assert "Dynamic slippage adjustment" in evolved.description


@pytest.mark.asyncio
async def test_startup_sequence_and_emergency_mode(tmp_path: Path):
    orchestrator = AgentOSOrchestrator(data_dir=tmp_path)

    # 1. Startup Sequence
    started = await orchestrator.run_startup_sequence()
    assert started is True
    assert orchestrator.startup_completed is True
    assert orchestrator.state == SystemState.NORMAL
    assert orchestrator.guardian is not None
    assert orchestrator.commander is not None
    assert orchestrator.trading is not None

    # 2. Trigger Emergency Mode
    state = await orchestrator.trigger_emergency_mode("Security threat detected in market order feed")
    assert state == SystemState.EMERGENCY_STOP
    assert orchestrator.trading.is_active is False
    assert orchestrator.devops.is_active is False
    assert (tmp_path / "emergency_logs" / "emergency_backup.log").exists()
    assert len(orchestrator.notifications) > 0
    assert orchestrator.notifications[0]["owner_notified"] is True

    # 3. Reset Emergency Mode
    res_state = await orchestrator.reset_emergency_mode()
    assert res_state == SystemState.NORMAL
    assert orchestrator.trading.is_active is True
