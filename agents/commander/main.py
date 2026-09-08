"""
GENX Agent Runtime Commander
Coordinates AI workers (Trader, Monitor, Security, Builder) and executes plans via SkillManager.
"""

import logging
from typing import Dict, Any, List, Optional
from src.skill_manager import SkillManager

logger = logging.getLogger(__name__)

class AgentCommander:
    """Commander agent managing worker execution and plan execution."""

    def __init__(self, skill_manager: Optional[SkillManager] = None):
        if skill_manager is None:
            self.skill_manager = SkillManager()
            self.skill_manager.discover_skills()
        else:
            self.skill_manager = skill_manager

        self.workers = ["commander", "trader", "monitor", "builder", "security_guard"]

    def execute_directive(self, goal: str) -> Dict[str, Any]:
        """Execute a directive goal by planning and running steps across skills."""
        logger.info(f"Agent Commander received directive: {goal}")

        # Plan the goal using agent_planner skill or fallback planning
        plan = []
        if "agent_planner" in self.skill_manager.registry:
            plan_res = self.skill_manager.execute_skill("agent_planner", {"goal": goal})
            plan = plan_res.get("plan", [])

        results = []
        for item in plan:
            skill_name = item.get("skill")
            action = item.get("action")
            if skill_name in self.skill_manager.registry:
                try:
                    res = self.skill_manager.execute_skill(skill_name, {"action": action, "goal": goal})
                    results.append({"step": item.get("step"), "skill": skill_name, "status": "executed", "result": res})
                except Exception as e:
                    results.append({"step": item.get("step"), "skill": skill_name, "status": "failed", "error": str(e)})

        return {
            "status": "completed",
            "goal": goal,
            "workers_available": self.workers,
            "plan": plan,
            "execution_results": results
        }


def run(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    commander = AgentCommander()
    goal = payload.get("goal", "Execute default trading check") if payload else "Execute default trading check"
    return commander.execute_directive(goal)
