"""Mini PC Device Worker Agent - Local AI Server."""

import logging
from typing import Dict, Any
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task
from agents.common.message_bus import MessageBus

logger = logging.getLogger(__name__)


class MiniPCAgent(BaseAgent):
    """Mini PC Agent - Runs local models, local database, trading bridge, and automation."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="MiniPCWorker",
            role="Local AI Server Node",
            default_permission=PermissionLevel.LEVEL_2_CREATE_FILES,
            message_bus=message_bus,
        )

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        action = task.parameters.get("action")
        if action == "RUN_LOCAL_MODEL":
            model_name = task.parameters.get("model", "llama-local")
            prompt = task.parameters.get("prompt", "")
            logger.info(f"Mini PC running local AI model '{model_name}'...")
            return {
                "node": self.name,
                "model": model_name,
                "response": f"Local AI inference response for '{prompt}'",
            }
        elif action == "LOCAL_DB_SYNC":
            return {"node": self.name, "status": "DB_SYNC_COMPLETED"}

        return {"status": "COMPLETED", "node": self.name, "message": f"Mini PC processed '{task.title}'"}
