"""AI Secret Guardian - Watches AI agents and blocks secret exposure."""

import re
import logging
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class AISecretGuardian:
    """Monitors AI agent outputs, commands, and code generation to prevent secret leaks."""

    SECRET_PATTERNS = [
        r"private_key\s*=\s*['\"].+['\"]",
        r"api_key\s*=\s*['\"].+['\"]",
        r"BEGIN PRIVATE KEY",
        r"glrt-[a-zA-Z0-9_\-\.]{20,}",
        r"AIzaSy[a-zA-Z0-9_\-]{33}",
    ]

    def __init__(self):
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.SECRET_PATTERNS]
        self.audit_count = 0

    def inspect_agent_action(self, agent_name: str, action_text: str) -> Tuple[bool, str]:
        """Inspect action/code text for secret exposure attempts."""
        self.audit_count += 1
        for pattern in self._compiled_patterns:
            if pattern.search(action_text):
                event_id = f"AUDIT-2026-{self.audit_count:05d}"
                logger.critical(f"BLOCKED ❌ Private key/secret exposure detected from agent '{agent_name}'. Event: {event_id}")
                return False, f"BLOCKED: Private key/secret exposure detected. Event: {event_id}"

        return True, "SAFE"
