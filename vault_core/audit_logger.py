"""Audit Logger for GENX Vault."""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AuditLogger:
    """Logs all secret access, rotation, and denied attempts into audit.log."""

    def __init__(self, log_path: str = "logs/audit.log"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log_event(self, event_type: str, agent_name: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Record audit event to log file."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "details": details,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"Audit Logged [{event_type}] for '{agent_name}'")
        return entry
