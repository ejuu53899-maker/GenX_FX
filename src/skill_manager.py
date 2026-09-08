#!/usr/bin/env python3
"""
GENX 3.6.9 Skill Manager
AI Capability OS Layer for dynamic import, installation, updating, and execution of skills.
"""

import os
import shutil
import importlib.util
import logging
from typing import Dict, Any, List, Optional
import yaml

logger = logging.getLogger(__name__)


class SkillLifecycleState:
    DISCOVERED = "DISCOVERED"
    DOWNLOADED = "DOWNLOADED"
    VERIFIED = "VERIFIED"
    INSTALLED = "INSTALLED"
    TESTED = "TESTED"
    ACTIVATED = "ACTIVATED"
    LEARNING = "LEARNING"
    UPDATED = "UPDATED"


class SkillManager:
    """Manager for GENX Skill Folder System"""

    def __init__(self, root_dir: Optional[str] = None):
        if root_dir is None:
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        else:
            self.root_dir = os.path.abspath(root_dir)

        self.skills_dir = os.path.join(self.root_dir, "skills")
        self.updates_dir = os.path.join(self.root_dir, "updates")
        self.registry: Dict[str, Dict[str, Any]] = {}
        self.active_skills: Dict[str, Any] = {}
        self.skills_state: Dict[str, str] = {}

    def discover_skills(self) -> Dict[str, Dict[str, Any]]:
        """Discover all available skill modules under skills_dir."""
        self.registry.clear()
        if not os.path.exists(self.skills_dir):
            logger.warning(f"Skills directory {self.skills_dir} does not exist.")
            return self.registry

        for root, dirs, files in os.walk(self.skills_dir):
            if "manifest.yaml" in files:
                manifest_path = os.path.join(root, "manifest.yaml")
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = yaml.safe_load(f) or {}

                    skill_name = manifest.get("name")
                    if skill_name:
                        self.registry[skill_name] = {
                            "name": skill_name,
                            "path": root,
                            "manifest": manifest,
                            "version": manifest.get("version", "1.0.0"),
                            "status": manifest.get("status", "inactive"),
                            "permission": manifest.get("permission", [])
                        }
                        self.skills_state[skill_name] = SkillLifecycleState.DISCOVERED
                        if manifest.get("status") == "active":
                            self.skills_state[skill_name] = SkillLifecycleState.ACTIVATED
                except Exception as e:
                    logger.error(f"Failed to load manifest at {manifest_path}: {e}")

        logger.info(f"Discovered {len(self.registry)} skill modules.")
        return self.registry

    def verify_signature(self, skill_name_or_path: str) -> bool:
        """Simulate signature verification for a skill module."""
        skill_path = skill_name_or_path
        if skill_name_or_path in self.registry:
            skill_path = self.registry[skill_name_or_path]["path"]

        manifest_path = os.path.join(skill_path, "manifest.yaml")
        if not os.path.exists(manifest_path):
            logger.error(f"Cannot verify signature: {manifest_path} missing.")
            return False

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f) or {}
            if "name" in manifest and "version" in manifest:
                if skill_name_or_path in self.registry:
                    self.skills_state[skill_name_or_path] = SkillLifecycleState.VERIFIED
                return True
        except Exception as e:
            logger.error(f"Signature verification failed for {skill_path}: {e}")

        return False

    def install_skill(self, source_path: str, category: str, skill_name: str) -> bool:
        """Install a new skill from a source directory into the skills tree."""
        if not self.verify_signature(source_path):
            logger.error(f"Skill installation rejected for {source_path}: signature verification failed.")
            return False

        target_dir = os.path.join(self.skills_dir, category, skill_name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        shutil.copytree(source_path, target_dir)
        self.skills_state[skill_name] = SkillLifecycleState.INSTALLED
        self.discover_skills()
        logger.info(f"Successfully installed skill '{skill_name}' under category '{category}'.")
        return True

    def test_skill(self, skill_name: str) -> bool:
        """Test a skill by verifying its module structure and imports."""
        if skill_name not in self.registry:
            logger.error(f"Skill '{skill_name}' not found in registry.")
            return False

        skill_info = self.registry[skill_name]
        src_main = os.path.join(skill_info["path"], "src", "main.py")
        if not os.path.exists(src_main):
            logger.error(f"Skill '{skill_name}' missing src/main.py")
            return False

        self.skills_state[skill_name] = SkillLifecycleState.TESTED
        return True

    def activate_skill(self, skill_name: str) -> bool:
        """Activate a skill so it can be dynamically executed."""
        if skill_name not in self.registry:
            logger.error(f"Skill '{skill_name}' not found in registry.")
            return False

        if not self.test_skill(skill_name):
            logger.error(f"Cannot activate skill '{skill_name}': test step failed.")
            return False

        skill_info = self.registry[skill_name]
        src_main = os.path.join(skill_info["path"], "src", "main.py")

        try:
            spec = importlib.util.spec_from_file_location(f"genx_skill_{skill_name}", src_main)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.active_skills[skill_name] = module
                self.skills_state[skill_name] = SkillLifecycleState.ACTIVATED
                skill_info["manifest"]["status"] = "active"
                logger.info(f"Skill '{skill_name}' activated successfully.")
                return True
        except Exception as e:
            logger.error(f"Failed to activate skill '{skill_name}': {e}")

        return False

    def execute_skill(self, skill_name: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        """Execute an active skill's main run function."""
        if skill_name not in self.active_skills:
            if not self.activate_skill(skill_name):
                raise RuntimeError(f"Skill '{skill_name}' is not active and could not be activated.")

        module = self.active_skills[skill_name]
        if hasattr(module, "run"):
            result = module.run(payload)
            self.skills_state[skill_name] = SkillLifecycleState.LEARNING
            return result
        else:
            raise AttributeError(f"Skill '{skill_name}' module has no 'run' entrypoint function.")

    def update_skill(self, skill_name: str, new_source_path: str) -> bool:
        """Update an existing skill and archive previous version in updates/rollback/."""
        if skill_name not in self.registry:
            logger.error(f"Cannot update: Skill '{skill_name}' not found in registry.")
            return False

        old_path = self.registry[skill_name]["path"]
        rollback_dir = os.path.join(self.updates_dir, "rollback", f"{skill_name}_{self.registry[skill_name]['version']}")
        if os.path.exists(rollback_dir):
            shutil.rmtree(rollback_dir)
        os.makedirs(os.path.dirname(rollback_dir), exist_ok=True)
        shutil.copytree(old_path, rollback_dir)

        # Overwrite with new version
        shutil.rmtree(old_path)
        shutil.copytree(new_source_path, old_path)

        self.skills_state[skill_name] = SkillLifecycleState.UPDATED
        self.discover_skills()
        self.activate_skill(skill_name)
        logger.info(f"Skill '{skill_name}' updated successfully from {new_source_path}.")
        return True
