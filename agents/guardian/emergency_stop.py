"""Emergency Stop mechanism for Guardian Agent."""

import logging
from agents.common.schemas import SystemState

logger = logging.getLogger(__name__)


class EmergencyStopController:
    """Manages emergency stop transitions and safeguards."""

    def __init__(self):
        self.current_state: SystemState = SystemState.NORMAL

    def trigger_emergency_stop(self, reason: str) -> SystemState:
        """Trigger immediate emergency stop across the entire system."""
        self.current_state = SystemState.EMERGENCY_STOP
        logger.critical(f"🚨 EMERGENCY STOP TRIGGERED: {reason}")
        return self.current_state

    def reset_system_state(self) -> SystemState:
        """Reset system state to NORMAL after verification."""
        self.current_state = SystemState.NORMAL
        logger.info("System state reset to NORMAL.")
        return self.current_state
