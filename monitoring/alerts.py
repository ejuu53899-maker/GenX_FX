"""Security Alerts Dispatcher."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SecurityAlerts:
    """Sends alerts on unauthorized secret requests or AI guardian triggers."""

    def dispatch_alert(self, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        logger.critical(f"SECURITY ALERT DISPATCHED [{event_type}]: {details}")
        return {"status": "ALERT_SENT", "event_type": event_type}
