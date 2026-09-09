"""Master Vault Engine for GENX Vault Manager v3.6.9+."""

import os
import json
import logging
from typing import Dict, Any, Optional
from .encryption import VaultEncryption
from .key_manager import KeyManager
from .policy_engine import VaultPolicyEngine
from .audit_logger import AuditLogger

logger = logging.getLogger(__name__)


class VaultEngine:
    """Master Security Controller for storing, retrieving, and rotating encrypted secrets."""

    def __init__(self, vault_dir: str = "vault/encrypted", log_file: str = "logs/audit.log"):
        self.vault_dir = vault_dir
        os.makedirs(vault_dir, exist_ok=True)

        self.encryption = VaultEncryption()
        self.key_manager = KeyManager(vault_dir)
        self.policy_engine = VaultPolicyEngine()
        self.audit_logger = AuditLogger(log_file)
        self._secrets_store: Dict[str, Dict[str, Any]] = {}

    def store_secret(self, key: str, value: str, owner: str = "GENX-Vault", expires_days: int = 180) -> bool:
        """Encrypt and store secret in vault."""
        encrypted_val = self.encryption.encrypt_secret(value)
        record = {
            "id": key,
            "owner": owner,
            "encrypted_value": encrypted_val,
            "status": "active",
            "expires_days": expires_days,
        }
        self._secrets_store[key] = record

        file_path = os.path.join(self.vault_dir, f"{key}.enc")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        self.audit_logger.log_event("SECRET_STORED", owner, {"secret_id": key})
        return True

    def get_secret(self, key: str, agent_name: str, action: str = "read_dev_env") -> Optional[str]:
        """Request secret access subject to policy engine checks."""
        if not self.policy_engine.check_permission(agent_name, action):
            self.audit_logger.log_event("ACCESS_DENIED", agent_name, {"secret_id": key, "reason": "Policy check failed"})
            return None

        record = self._secrets_store.get(key)
        if not record:
            file_path = os.path.join(self.vault_dir, f"{key}.enc")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    record = json.load(f)
                    self._secrets_store[key] = record

        if not record:
            logger.warning(f"Secret '{key}' not found in vault.")
            return None

        decrypted = self.encryption.decrypt_secret(record["encrypted_value"])
        self.audit_logger.log_event("SECRET_READ", agent_name, {"secret_id": key})
        return decrypted
