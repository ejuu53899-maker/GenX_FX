"""Docker Manager for DevOps Agent."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DockerManager:
    """Manages Docker container status and lifecycle."""

    def __init__(self):
        self._containers = {"genx_api": "running", "genx_db": "running", "genx_redis": "running"}

    def get_container_statuses(self) -> Dict[str, str]:
        """Return statuses of managed containers."""
        return dict(self._containers)

    def restart_container(self, container_name: str) -> Dict[str, Any]:
        """Restart a failed container."""
        if container_name in self._containers:
            self._containers[container_name] = "running"
            logger.info(f"Container '{container_name}' restarted successfully.")
            return {"status": "RESTARTED", "container": container_name}
        return {"status": "ERROR", "reason": f"Container '{container_name}' not found."}
