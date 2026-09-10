"""USB Storage Management Module for GENX CLI."""


def scan_storage() -> str:
    """Return USB storage status."""
    return """========================================
              USB STORAGE
========================================
BLUEDIM64GB
Purpose: AI Boot / Recovery
Status:  ACTIVE

ADATA32GB
Purpose: Backup / Vault
Status:  CONNECTED"""
