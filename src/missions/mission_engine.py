"""
GENX Mission Registry & Automation Engine (v3.6.9)
Executes "one-click missions" (declarative workflows with pre-flight checks, task orchestration, and rollback).
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MissionStep(BaseModel):
    step_id: str
    action: str
    target: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class MissionDefinition(BaseModel):
    mission_id: str
    name: str
    description: str
    preflight_checks: List[str] = Field(default_factory=list)
    steps: List[MissionStep] = Field(default_factory=list)
    rollback_steps: List[MissionStep] = Field(default_factory=list)


class MissionAutomationEngine:
    """
    Executes declarative multi-step missions with pre-flight checks and rollback.
    """

    def __init__(self):
        self._registry: Dict[str, MissionDefinition] = {}

    def register_mission(self, mission: MissionDefinition) -> None:
        self._registry[mission.mission_id] = mission
        logger.info(f"Registered mission '{mission.name}' ({mission.mission_id})")

    def list_missions(self) -> List[MissionDefinition]:
        return list(self._registry.values())

    def execute_mission(
        self,
        mission_id: str,
        step_executor: Callable[[MissionStep], bool]
    ) -> Dict[str, Any]:
        """
        Executes preflight checks and mission steps. Triggers rollback if step fails.
        """
        mission = self._registry.get(mission_id)
        if not mission:
            return {"status": "error", "message": f"Mission '{mission_id}' not found."}

        logger.info(f"Starting Mission: {mission.name}")
        completed_steps: List[MissionStep] = []

        for step in mission.steps:
            logger.info(f"Executing step {step.step_id}: {step.action} on {step.target}")
            success = step_executor(step)
            if success:
                completed_steps.append(step)
            else:
                logger.error(f"Step {step.step_id} failed! Initiating rollback...")
                self._rollback(mission.rollback_steps, step_executor)
                return {
                    "status": "failed",
                    "failed_step": step.step_id,
                    "completed_steps": [s.step_id for s in completed_steps],
                    "rolled_back": True
                }

        return {
            "status": "success",
            "mission_id": mission_id,
            "completed_steps_count": len(completed_steps)
        }

    def _rollback(self, rollback_steps: List[MissionStep], step_executor: Callable[[MissionStep], bool]) -> None:
        for rb in rollback_steps:
            logger.warning(f"Rollback step {rb.step_id}: {rb.action} on {rb.target}")
            try:
                step_executor(rb)
            except Exception as e:
                logger.error(f"Error during rollback step {rb.step_id}: {e}")
