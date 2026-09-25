"""Guardian Agent - Security + Safety Agent."""

import logging
from typing import Dict, Any, Optional
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, AgentMessage, Task
from agents.common.message_bus import MessageBus

from .access_control import AccessControlManager
from .secret_manager import SecretManager
from .threat_detection import ThreatDetectionSystem
from .backup_check import BackupChecker
from .emergency_stop import EmergencyStopController

logger = logging.getLogger(__name__)


class GuardianAgent(BaseAgent):
    """Guardian Agent overseeing security, secrets, threat detection, and emergency stops."""

    def __init__(self, message_bus: MessageBus):
        super().__init__(
            name="Guardian",
            role="Security + Safety Agent",
            default_permission=PermissionLevel.LEVEL_5_FINANCIAL_OPERATIONS,
            message_bus=message_bus,
        )
        self.access_control = AccessControlManager()
        self.secret_manager = SecretManager()
        self.threat_detection = ThreatDetectionSystem()
        self.backup_checker = BackupChecker()
        self.emergency_stop = EmergencyStopController()

        # Subscribe to security audit and risk requests
        self.bus.subscribe("guardian.security_check", self._handle_security_check)
        self.bus.subscribe("guardian.emergency_stop", self._handle_emergency_trigger)

    async def _handle_security_check(self, message: AgentMessage) -> None:
        """Handle security check request."""
        activity_type = message.payload.get("activity_type", "")
        details = message.payload.get("details", {})
        agent_name = message.sender

        is_threat = self.threat_detection.evaluate_activity(activity_type, details)
        if is_threat:
            logger.warning(f"Guardian blocking action from '{agent_name}' due to threat policy.")
            await self.send_message(
                receiver=agent_name,
                topic="guardian.security_response",
                payload={"approved": False, "reason": "Threat detected by Guardian Agent"},
            )
            # If severe threat, trigger emergency stop
            if message.payload.get("severity") == "CRITICAL":
                await self.trigger_emergency_stop("Critical security threat detected")
        else:
            await self.send_message(
                receiver=agent_name,
                topic="guardian.security_response",
                payload={"approved": True, "reason": "Security check passed"},
            )

    async def _handle_emergency_trigger(self, message: AgentMessage) -> None:
        reason = message.payload.get("reason", "Emergency stop requested via message bus")
        await self.trigger_emergency_stop(reason)

    async def trigger_emergency_stop(self, reason: str) -> None:
        """Execute emergency stop broadcast across network."""
        state = self.emergency_stop.trigger_emergency_stop(reason)
        await self.send_message(
            receiver="ALL",
            topic="system.broadcast",
            payload={"event": "EMERGENCY_STOP", "state": state.value, "reason": reason},
            level_required=PermissionLevel.LEVEL_4_EXECUTE_ACTIONS,
        )

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        """Process tasks assigned to Guardian Agent."""
        action = task.parameters.get("action")
        if action == "CHECK_BACKUP":
            from pathlib import Path
            path = Path(task.parameters.get("path", "data"))
            return self.backup_checker.verify_backup_integrity(path)
        elif action == "STORE_SECRET":
            key = task.parameters.get("key")
            val = task.parameters.get("value")
            self.secret_manager.store_secret(key, val)
            return {"status": "SECRET_STORED", "key": key}
        elif action == "EMERGENCY_STOP":
            reason = task.parameters.get("reason", "Manual emergency stop task")
            await self.trigger_emergency_stop(reason)
            return {"status": "EMERGENCY_STOP_ACTIVE"}

        return {"status": "COMPLETED", "message": f"Guardian processed task '{task.title}'"}
