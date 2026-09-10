"""Secret Manager for Guardian Agent - Ensures secrets are never exposed."""

import logging
from typing import Dict, Optional
import re

logger = logging.getLogger(__name__)


class SecretManager:
    """Manages sensitive API credentials and sanitizes log outputs."""

    def __init__(self):
        self._secrets: Dict[str, str] = {}

    def store_secret(self, key: str, value: str) -> None:
        """Store a sensitive key/value pair."""
        self._secrets[key] = value
        logger.info(f"Secret key '{key}' securely stored.")

    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve secret by key."""
        return self._secrets.get(key)

    def sanitize_output(self, text: str) -> str:
        """Sanitize text to redact any stored secret values."""
        sanitized = text
        for secret_val in self._secrets.values():
            if secret_val and len(secret_val) > 3:
                sanitized = sanitized.replace(secret_val, "***REDACTED***")
        return sanitized
