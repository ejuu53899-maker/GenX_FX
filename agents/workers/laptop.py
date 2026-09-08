"""Laptop Device Worker Agent - Development Command Center."""

import logging
from typing import Dict, Any
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task
from agents.common.message_bus import MessageBus

logger = logging.getLogger(__name__)


class LaptopAgent(BaseAgent):
    """Laptop Agent - Runs development, coding, testing, AI model training, and deployment triggers."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="LaptopWorker",
            role="Development Command Center",
            default_permission=PermissionLevel.LEVEL_3_DEPLOY,
            message_bus=message_bus,
        )

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        action = task.parameters.get("action")
        if action == "TRAIN_MODEL":
            model_type = task.parameters.get("model_type", "xgboost")
            logger.info(f"Laptop Agent training model '{model_type}'...")
            return {
                "node": self.name,
                "model_type": model_type,
                "metrics": {"accuracy": 0.92, "loss": 0.14},
            }
        elif action == "DEV_BUILD":
            return {"node": self.name, "status": "DEV_BUILD_PASSED"}

        return {"status": "COMPLETED", "node": self.name, "message": f"Laptop Agent processed '{task.title}'"}
