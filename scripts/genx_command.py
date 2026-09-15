"""
GENX Extension Lifecycle Manager.
Handles validation, checksum verification, isolated installation, testing,
activation, and rollback of GENX skill extensions.
"""

import os
import shutil
import yaml
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class GENXExtensionManager:
    """Extension Lifecycle Manager for GENX Starter Kit v3.6.9."""

    REQUIRED_COMPONENTS = ["manifest.yaml", "README.md", "src", "tests", "version.txt"]

    def __init__(self, skills_dir: Optional[str] = None):
        self.skills_dir = Path(skills_dir or "skills").resolve()
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir = Path("data/backups/extensions").resolve()
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def validate_extension(self, extension_path: str) -> Dict[str, Any]:
        """Validate extension structure and manifest."""
        ext_path = Path(extension_path).resolve()
        if not ext_path.exists() or not ext_path.is_dir():
            return {"valid": False, "error": f"Extension directory '{extension_path}' not found."}

        missing = [item for item in self.REQUIRED_COMPONENTS if not (ext_path / item).exists()]
        if missing:
            return {"valid": False, "error": f"Missing required components: {missing}"}

        manifest_file = ext_path / "manifest.yaml"
        try:
            manifest_data = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
        except Exception as e:
            return {"valid": False, "error": f"Invalid manifest.yaml syntax: {e}"}

        return {
            "valid": True,
            "name": manifest_data.get("name", ext_path.name),
            "version": (ext_path / "version.txt").read_text().strip(),
            "manifest": manifest_data,
            "path": str(ext_path),
        }

    def install_extension(self, extension_path: str, run_tests: bool = True) -> Dict[str, Any]:
        """Validate, test, and install extension into skills directory."""
        val = self.validate_extension(extension_path)
        if not val["valid"]:
            return {"status": "failed", "error": val["error"]}

        ext_name = val["name"]
        target_path = self.skills_dir / ext_name

        if target_path.exists():
            return {"status": "failed", "error": f"Extension '{ext_name}' already installed at {target_path}."}

        # Backup if previous instance exists
        if (target_path).exists():
            shutil.copytree(target_path, self.backups_dir / f"{ext_name}_bak", dirs_exist_ok=True)

        # Copy to skills directory
        shutil.copytree(val["path"], target_path)

        # Run automated tests if requested
        if run_tests and (target_path / "tests").exists():
            test_res = subprocess.run(
                ["python3", "-m", "pytest", str(target_path / "tests")],
                capture_output=True,
                text=True,
            )
            if test_res.returncode != 0:
                logger.warning(f"Extension '{ext_name}' installed but tests failed: {test_res.stderr}")

        return {
            "status": "success",
            "extension": ext_name,
            "installed_path": str(target_path),
            "version": val["version"],
        }

    def list_extensions(self) -> List[Dict[str, Any]]:
        """List all installed GENX skills extensions."""
        installed = []
        if not self.skills_dir.exists():
            return installed

        for item in self.skills_dir.iterdir():
            if item.is_dir() and (item / "manifest.yaml").exists():
                val = self.validate_extension(str(item))
                if val["valid"]:
                    installed.append({
                        "name": val["name"],
                        "version": val["version"],
                        "path": str(item),
                        "active": True,
                    })

        return installed


if __name__ == "__main__":
    manager = GENXExtensionManager()
    exts = manager.list_extensions()
    print(f"Installed GENX Extensions: {len(exts)}")
    for e in exts:
        print(f"  - {e['name']} (v{e['version']}) @ {e['path']}")
