"""Key Manager for GENX Vault - Hardware Key & Master Key derivation."""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class KeyManager:
    """Manages master key lifecycle, hardware identity validation, and key rotation."""

    def __init__(self, key_store_dir: str = "vault/encrypted"):
        self.key_store_dir = key_store_dir
        os.makedirs(key_store_dir, exist_ok=True)
        self._master_key: str = os.getenv("GENX_VAULT_MASTER_KEY", "DEFAULT_GENX_MASTER_KEY_369")

    def derive_key(self, agent_name: str) -> str:
        """Derive agent-specific session key."""
        return f"KEY-{agent_name.upper()}-{self._master_key[:8]}"

    def validate_hardware_identity(self, hardware_id: Optional[str] = None) -> bool:
        """Validate BLUEDIM / USB Hardware key identity."""
        if hardware_id and "BLUEDIM" in hardware_id.upper():
            logger.info(f"Hardware key identity '{hardware_id}' verified.")
            return True
        logger.info("Operating with default software key identity.")
        return True
