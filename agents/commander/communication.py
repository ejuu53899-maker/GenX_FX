"""Communication coordinator for Commander Agent."""

import logging
from typing import Dict, Any
from agents.common.schemas import AgentMessage, PermissionLevel
from agents.common.message_bus import MessageBus

logger = logging.getLogger(__name__)


class CommunicationCoordinator:
    """Manages routing and coordination of multi-agent communication."""

    def __init__(self, bus: MessageBus):
        self.bus = bus

    async def broadcast_command(self, topic: str, payload: Dict[str, Any]) -> None:
        """Broadcast command to all listening agents."""
        msg = AgentMessage(
            sender="Commander",
            receiver="ALL",
            topic=topic,
            payload=payload,
            level_required=PermissionLevel.LEVEL_1_ANALYZE,
        )
        await self.bus.publish(msg)

    async def send_direct_task(self, target_agent: str, task_data: Dict[str, Any]) -> None:
        """Send task message directly to specific target agent."""
        msg = AgentMessage(
            sender="Commander",
            receiver=target_agent,
            topic=f"agent.{target_agent}",
            payload={"type": "TASK_ASSIGNMENT", "task": task_data},
            level_required=PermissionLevel.LEVEL_1_ANALYZE,
        )
        await self.bus.publish(msg)
