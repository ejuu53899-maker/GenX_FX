"""State and Memory Manager for Commander Agent."""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class CommanderMemory:
    """Maintains system operational state, agent registration, and context memory."""

    def __init__(self):
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.system_status: Dict[str, Any] = {"mode": "NORMAL", "active_agents": 0}
        self.context_memory: Dict[str, Any] = {}

    def register_agent(self, name: str, role: str, status: str = "ONLINE") -> None:
        """Register an active agent in memory."""
        self.agent_registry[name] = {"role": role, "status": status}
        self.system_status["active_agents"] = len(self.agent_registry)
        logger.info(f"Agent '{name}' registered in Commander Memory. Total active: {len(self.agent_registry)}")

    def set_context(self, key: str, value: Any) -> None:
        """Store key value in operational context memory."""
        self.context_memory[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieve context value."""
        return self.context_memory.get(key, default)
