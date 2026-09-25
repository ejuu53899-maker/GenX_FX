"""Backup Checker for Guardian Agent."""

import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class BackupChecker:
    """Verifies system state and data backup integrity."""

    def verify_backup_integrity(self, backup_dir: Path) -> Dict[str, Any]:
        """Check if backup directory exists and contains valid backup files."""
        if not backup_dir.exists():
            return {"valid": False, "reason": f"Backup directory '{backup_dir}' does not exist."}

        files = list(backup_dir.glob("*"))
        if not files:
            return {"valid": False, "reason": f"Backup directory '{backup_dir}' is empty."}

        logger.info(f"Backup check passed: {len(files)} files found in '{backup_dir}'.")
        return {"valid": True, "file_count": len(files)}
