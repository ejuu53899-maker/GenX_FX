"""Secret Manager for Guardian Agent - Ensures secrets are never exposed."""

import logging
from typing import Dict, Optional, Tuple
from vault_core.vault_engine import VaultEngine
from security.ai_guardian import AISecretGuardian

logger = logging.getLogger(__name__)


class SecretManager:
    """Manages sensitive API credentials, encrypts via VaultEngine, and monitors leaks via AISecretGuardian."""

    def __init__(self):
        self.vault_engine = VaultEngine()
        self.ai_guardian = AISecretGuardian()
        self._secrets: Dict[str, str] = {}

    def store_secret(self, key: str, value: str, owner: str = "Guardian") -> None:
        """Store a sensitive key/value pair in encrypted vault."""
        self._secrets[key] = value
        self.vault_engine.store_secret(key, value, owner=owner)
        logger.info(f"Secret key '{key}' securely stored in GENX Vault.")

    def get_secret(self, key: str, requesting_agent: str = "guardian") -> Optional[str]:
        """Retrieve secret by key using vault policy engine."""
        return self.vault_engine.get_secret(key, agent_name=requesting_agent)

    def inspect_agent_action(self, agent_name: str, action_text: str) -> Tuple[bool, str]:
        """Inspect agent action text for potential secret leaks."""
        return self.ai_guardian.inspect_agent_action(agent_name, action_text)

    def sanitize_output(self, text: str) -> str:
        """Sanitize text to redact any stored secret values."""
        sanitized = text
        for secret_val in self._secrets.values():
            if secret_val and len(secret_val) > 3:
                sanitized = sanitized.replace(secret_val, "***REDACTED***")
        return sanitized
