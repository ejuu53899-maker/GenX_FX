"""DevOps Agent - Infrastructure Engineer."""

import logging
from typing import Dict, Any
from pathlib import Path
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task
from agents.common.message_bus import MessageBus

from .docker_manager import DockerManager
from .server_manager import ServerManager
from .deployment import DeploymentManager
from .monitoring import SystemMonitor
from .backup import AutomatedBackup

logger = logging.getLogger(__name__)


class DevOpsAgent(BaseAgent):
    """DevOps Agent responsible for infrastructure, deployments, containers, server health, and backups."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="DevOps",
            role="Infrastructure Engineer",
            default_permission=PermissionLevel.LEVEL_3_DEPLOY,
            message_bus=message_bus,
        )
        self.docker_manager = DockerManager()
        self.server_manager = ServerManager()
        self.deployment = DeploymentManager()
        self.monitoring = SystemMonitor()
        self.backup = AutomatedBackup()

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Execute DevOps tasks."""
        action = task.parameters.get("action")
        if action == "DEPLOY":
            service = task.parameters.get("feature", task.parameters.get("service", "app"))
            version = task.parameters.get("version", "1.0.0")
            return self.deployment.deploy_service(service, version)

        elif action == "RESTART_CONTAINER":
            container = task.parameters.get("container", "genx_api")
            return self.docker_manager.restart_container(container)

        elif action == "CHECK_SERVER_HEALTH":
            health = self.server_manager.get_server_health()
            uptime = self.monitoring.get_uptime_metrics()
            return {"server_health": health, "uptime_metrics": uptime}

        elif action == "CREATE_BACKUP":
            path = Path(task.parameters.get("path", "data/backups"))
            return self.backup.create_snapshot(path)

        return {"status": "COMPLETED", "message": f"DevOps processed task '{task.title}'"}
