"""In-memory asynchronous Agent Message Bus for GENX 3.6.9 Agent OS."""

import asyncio
import logging
from typing import Dict, List, Callable, Awaitable, Optional, Union
from collections import defaultdict
from .schemas import AgentMessage, PermissionLevel
from .permissions import PermissionManager

logger = logging.getLogger(__name__)

MessageHandler = Callable[[AgentMessage], Union[None, Awaitable[None]]]


class MessageBus:
    """Agent Message Bus for inter-agent communication."""

    def __init__(self, permission_manager: Optional[PermissionManager] = None):
        self.permission_manager = permission_manager or PermissionManager()
        self._subscribers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self._message_history: List[AgentMessage] = []

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """Subscribe a handler function to a topic."""
        if handler not in self._subscribers[topic]:
            self._subscribers[topic].append(handler)
            logger.debug(f"Subscribed handler to topic '{topic}'")

    def unsubscribe(self, topic: str, handler: MessageHandler) -> None:
        """Unsubscribe a handler from a topic."""
        if handler in self._subscribers[topic]:
            self._subscribers[topic].remove(handler)

    async def publish(self, message: AgentMessage) -> bool:
        """Publish a message to the bus after validating permissions."""
        # Permission check for sending messages
        if not self.permission_manager.has_permission(message.sender, message.level_required):
            logger.warning(
                f"Message publish blocked: '{message.sender}' lacks permission level {message.level_required.name}"
            )
            return False

        self._message_history.append(message)
        logger.info(f"Message Bus [Topic: {message.topic}] From: {message.sender} To: {message.receiver}")

        # Dispatch to topic subscribers
        handlers = list(self._subscribers.get(message.topic, []))
        # Dispatch to wildcards if topic is specific, or "ALL" subscribers
        if message.topic != "*":
            handlers.extend(self._subscribers.get("*", []))

        for handler in handlers:
            try:
                res = handler(message)
                if asyncio.iscoroutine(res):
                    await res
            except Exception as e:
                logger.error(f"Error handling message on topic '{message.topic}' by {handler}: {e}", exc_info=True)

        return True

    def get_history(self, topic: Optional[str] = None, limit: int = 50) -> List[AgentMessage]:
        """Retrieve recent message history."""
        if topic:
            filtered = [m for m in self._message_history if m.topic == topic or topic == "*"]
            return filtered[-limit:]
        return self._message_history[-limit:]

    def clear_history(self) -> None:
        """Clear message history."""
        self._message_history.clear()
