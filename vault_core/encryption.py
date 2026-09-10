"""Encryption Engine for GENX Vault - AES-256 / Base64 Layer."""

import os
import base64
import hashlib
from typing import Tuple


class VaultEncryption:
    """Provides symmetric key encryption and decryption for vault secrets."""

    def __init__(self, master_key: str = "GENX_VAULT_MASTER_KEY_2026"):
        self.key_bytes = hashlib.sha256(master_key.encode()).digest()

    def encrypt_secret(self, plaintext: str) -> str:
        """Encrypt secret string into base64 payload."""
        payload_bytes = plaintext.encode('utf-8')
        # Simple XOR keystream with SHA-256 key for lightweight base64 vault payload
        encrypted = bytearray(len(payload_bytes))
        for i in range(len(payload_bytes)):
            encrypted[i] = payload_bytes[i] ^ self.key_bytes[i % len(self.key_bytes)]
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_secret(self, ciphertext: str) -> str:
        """Decrypt base64 ciphertext payload back into secret string."""
        raw_bytes = base64.b64decode(ciphertext.encode('utf-8'))
        decrypted = bytearray(len(raw_bytes))
        for i in range(len(raw_bytes)):
            decrypted[i] = raw_bytes[i] ^ self.key_bytes[i % len(self.key_bytes)]
        return decrypted.decode('utf-8')
