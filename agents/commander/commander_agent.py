"""GENX Commander Agent - Central Brain."""

import logging
from typing import Dict, Any, List, Optional
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, AgentMessage, Task, SystemState
from agents.common.message_bus import MessageBus

from .planner import StrategicPlanner
from .decision_engine import DecisionEngine
from .memory import CommanderMemory
from .task_queue import TaskQueue
from .communication import CommunicationCoordinator

logger = logging.getLogger(__name__)


class CommanderAgent(BaseAgent):
    """Commander Agent coordinating all sub-agents, assigning tasks, and maintaining system state."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="Commander",
            role="Central Brain",
            default_permission=PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
            message_bus=message_bus,
        )
        self.planner = StrategicPlanner()
        self.decision_engine = DecisionEngine()
        self.memory = CommanderMemory()
        self.task_queue = TaskQueue()
        self.communication = CommunicationCoordinator(message_bus)
        self.system_state: SystemState = SystemState.NORMAL

        # Subscribe to agent responses and registration requests
        self.bus.subscribe("commander.register_agent", self._handle_agent_registration)
        self.bus.subscribe("commander.task_response", self._handle_task_response)

    async def _handle_agent_registration(self, message: AgentMessage) -> None:
        agent_name = message.sender
        role = message.payload.get("role", "Unknown")
        self.memory.register_agent(agent_name, role)
        logger.info(f"Commander registered agent: {agent_name} ({role})")

    async def _handle_task_response(self, message: AgentMessage) -> None:
        task_id = message.payload.get("task_id")
        status = message.payload.get("status")
        result = message.payload.get("result")
        logger.info(f"Commander received task response for task {task_id} from {message.sender}: {status}")

    async def plan_and_dispatch_goal(self, goal: str, context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """Create execution plan for a goal and enqueue tasks."""
        if self.system_state == SystemState.EMERGENCY_STOP:
            logger.error("Cannot dispatch goals while system is in EMERGENCY_STOP state.")
            return []

        ctx = context or {}
        tasks = self.planner.create_execution_plan(goal, ctx)
        for task in tasks:
            # Check safety
            safe, reason = self.decision_engine.evaluate_safety(
                task.title, task.parameters, self.default_permission
            )
            if not safe:
                logger.warning(f"Task '{task.title}' blocked by Decision Engine: {reason}")
                task.status = "CANCELLED"
                task.result = {"error": reason}
                continue

            self.task_queue.add_task(task)
            await self.communication.send_direct_task(task.assigned_agent, task.model_dump())
        return tasks

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Run tasks assigned to Commander."""
        action = task.parameters.get("action")
        if action == "PROCESS_GOAL":
            goal = task.parameters.get("goal", "")
            dispatched = await self.plan_and_dispatch_goal(goal, task.parameters)
            return {"dispatched_tasks_count": len(dispatched)}
        return {"status": "COMPLETED", "message": f"Commander processed task '{task.title}'"}
