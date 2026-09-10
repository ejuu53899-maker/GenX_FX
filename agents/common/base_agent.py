"""Base Agent class for GENX 3.6.9 Agent OS."""

import logging
from typing import Dict, Any, Optional, List
from .schemas import PermissionLevel, AgentMessage, Task, Skill, Experience
from .message_bus import MessageBus
from .permissions import PermissionManager

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all GENX autonomous agents."""

    def __init__(
        self,
        name: str,
        role: str,
        default_permission: PermissionLevel,
        message_bus: MessageBus,
        permission_manager: Optional[PermissionManager] = None,
    ):
        self.name = name
        self.role = role
        self.default_permission = default_permission
        self.bus = message_bus
        self.permission_manager = permission_manager or message_bus.permission_manager
        self.permission_manager.register_agent_permission(self.name, self.default_permission)

        self.skills: Dict[str, Skill] = {}
        self.experiences: List[Experience] = []
        self.is_active: bool = True

        # Subscribe agent to its own direct messages topic
        self.bus.subscribe(f"agent.{self.name}", self._handle_direct_message)
        # Subscribe agent to system broadcasts
        self.bus.subscribe("system.broadcast", self.on_system_broadcast)

        logger.info(f"Agent '{self.name}' ({self.role}) initialized with level {self.default_permission.name}.")

    async def send_message(
        self,
        receiver: str,
        topic: str,
        payload: Dict[str, Any],
        level_required: PermissionLevel = PermissionLevel.LEVEL_0_READ_ONLY,
    ) -> bool:
        """Send a message to another agent or broadcast topic."""
        msg = AgentMessage(
            sender=self.name,
            receiver=receiver,
            topic=topic,
            payload=payload,
            level_required=level_required,
        )
        return await self.bus.publish(msg)

    async def _handle_direct_message(self, message: AgentMessage) -> None:
        """Internal direct message handler wrapper."""
        if not self.is_active:
            logger.warning(f"Agent '{self.name}' is inactive, ignoring direct message.")
            return
        await self.on_message(message)

    async def on_message(self, message: AgentMessage) -> None:
        """Override in subclasses to handle incoming messages."""
        logger.debug(f"[{self.name}] Received message on topic '{message.topic}' from '{message.sender}'")

    async def on_system_broadcast(self, message: AgentMessage) -> None:
        """Override in subclasses to handle system broadcasts (e.g. emergency stop)."""
        logger.info(f"[{self.name}] System broadcast received: {message.payload}")

    def check_permission(self, level: PermissionLevel) -> bool:
        """Check if this agent possesses a specific permission level."""
        return self.permission_manager.has_permission(self.name, level)

    def import_skill(self, skill: Skill) -> bool:
        """Import a new skill package into the agent's capability library."""
        if not self.check_permission(skill.required_level):
            logger.error(f"Agent '{self.name}' lacks permission {skill.required_level.name} to import skill '{skill.name}'.")
            return False

        self.skills[skill.skill_id] = skill
        logger.info(f"Skill '{skill.name}' v{skill.version} imported into agent '{self.name}'.")
        return True

    async def execute_task(self, task: Task) -> Task:
        """Execute assigned task if permission allows."""
        if not self.is_active:
            task.status = "CANCELLED"
            task.result = {"error": f"Agent '{self.name}' is inactive."}
            return task

        if not self.check_permission(task.required_level):
            task.status = "FAILED"
            task.result = {"error": f"Permission denied for level {task.required_level.name}"}
            return task

        task.status = "IN_PROGRESS"
        try:
            result = await self.run_task_logic(task)
            task.status = "COMPLETED"
            task.result = result
            self.record_experience(
                action=task.title,
                result=result or {},
                status="SUCCESS",
                analysis="Task executed successfully.",
            )
        except Exception as e:
            logger.error(f"Error executing task '{task.task_id}' by '{self.name}': {e}", exc_info=True)
            task.status = "FAILED"
            task.result = {"error": str(e)}
            self.record_experience(
                action=task.title,
                result={"error": str(e)},
                status="FAILURE",
                analysis=f"Exception encountered: {e}",
            )
        return task

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Override in subclasses to perform specific task execution."""
        return {"message": f"Task '{task.title}' processed by {self.name}"}

    def record_experience(
        self,
        action: str,
        result: Dict[str, Any],
        status: str,
        analysis: Optional[str] = None,
        improvement_plan: Optional[str] = None,
    ) -> Experience:
        """Record an experience entry for the agent learning loop."""
        exp = Experience(
            agent_name=self.name,
            action=action,
            result=result,
            status=status,
            analysis=analysis,
            improvement_plan=improvement_plan,
        )
        self.experiences.append(exp)
        return exp
