"""Threat Detection System for Guardian Agent."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ThreatDetectionSystem:
    """Monitors metrics and logs for potential security threats or anomalous behavior."""

    def __init__(self):
        self.threat_log: List[Dict[str, Any]] = []

    def evaluate_activity(self, activity_type: str, details: Dict[str, Any]) -> bool:
        """Evaluate if an activity poses a security threat."""
        is_threat = False
        reason = ""

        if activity_type == "TRADE_EXECUTION":
            lot_size = details.get("lot_size", 0.0)
            if lot_size > 50.0:  # Excessive risk threshold
                is_threat = True
                reason = f"Abnormally high trade size requested: {lot_size} lots"

        elif activity_type == "FILE_ACCESS":
            path = details.get("filepath", "")
            if ".env" in path or "secrets" in path:
                is_threat = True
                reason = f"Unauthorized access attempt to sensitive file: {path}"

        if is_threat:
            entry = {"activity_type": activity_type, "details": details, "reason": reason}
            self.threat_log.append(entry)
            logger.error(f"THREAT DETECTED: {reason}")

        return is_threat
