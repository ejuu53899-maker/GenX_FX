"""
Unit tests for Mission Automation Engine.
"""

import pytest
from src.missions.mission_engine import MissionAutomationEngine, MissionDefinition, MissionStep


def test_mission_execution_success():
    engine = MissionAutomationEngine()
    mission = MissionDefinition(
        mission_id="M01",
        name="Test Mission",
        description="Testing mission workflow",
        steps=[
            MissionStep(step_id="s1", action="start", target="VPS"),
            MissionStep(step_id="s2", action="connect", target="MT5")
        ]
    )
    engine.register_mission(mission)

    res = engine.execute_mission("M01", step_executor=lambda step: True)
    assert res["status"] == "success"
    assert res["completed_steps_count"] == 2


def test_mission_execution_failure_rollback():
    engine = MissionAutomationEngine()
    mission = MissionDefinition(
        mission_id="M02",
        name="Failing Mission",
        description="Testing mission failure rollback",
        steps=[
            MissionStep(step_id="s1", action="start", target="VPS"),
            MissionStep(step_id="s2", action="fail", target="MT5")
        ],
        rollback_steps=[
            MissionStep(step_id="rb1", action="stop", target="VPS")
        ]
    )
    engine.register_mission(mission)

    def mock_executor(step: MissionStep) -> bool:
        return step.action != "fail"

    res = engine.execute_mission("M02", step_executor=mock_executor)
    assert res["status"] == "failed"
    assert res["rolled_back"] is True
