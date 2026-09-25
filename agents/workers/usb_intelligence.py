"""USB Intelligence Device Worker Agent - Portable Skill Installer."""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from agents.common.base_agent import BaseAgent
from agents.common.schemas import PermissionLevel, Task, Skill
from agents.common.message_bus import MessageBus

logger = logging.getLogger(__name__)


class USBIntelligenceAgent(BaseAgent):
    """USB Intelligence Agent - Portable Skill Installer, carries skills, backs up configuration, restores systems."""

    def __init__(self, message_bus: MessageBus, usb_mount_path: Path = Path("data/usb_drive")):
        super().__init__(
            name="USBIntelligenceWorker",
            role="Portable Skill Installer",
            default_permission=PermissionLevel.LEVEL_2_CREATE_FILES,
            message_bus=message_bus,
        )
        self.usb_mount_path = usb_mount_path
        self.usb_mount_path.mkdir(parents=True, exist_ok=True)

    def export_skill_package(self, skill: Skill) -> Path:
        """Export a skill to USB storage package."""
        pkg_path = self.usb_mount_path / f"skill_{skill.skill_id}.json"
        pkg_path.write_text(json.dumps(skill.model_dump(), indent=2), encoding="utf-8")
        logger.info(f"Skill '{skill.name}' exported to USB package: '{pkg_path}'")
        return pkg_path

    def load_skill_packages_from_usb(self) -> List[Skill]:
        """Load skill packages stored in USB storage."""
        skills: List[Skill] = []
        for file in self.usb_mount_path.glob("skill_*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                skill = Skill(**data)
                skills.append(skill)
                logger.info(f"Loaded skill package '{skill.name}' from USB.")
            except Exception as e:
                logger.error(f"Error reading skill package '{file}': {e}")
        return skills

    def backup_system_configuration(self, config_data: Dict[str, Any]) -> Path:
        """Backup system configuration to USB drive."""
        backup_path = self.usb_mount_path / "system_config_backup.json"
        backup_path.write_text(json.dumps(config_data, indent=2), encoding="utf-8")
        logger.info(f"System configuration backed up to USB: '{backup_path}'")
        return backup_path

    def restore_system_configuration(self) -> Optional[Dict[str, Any]]:
        """Restore configuration from USB drive."""
        backup_path = self.usb_mount_path / "system_config_backup.json"
        if not backup_path.exists():
            logger.warning(f"No USB backup found at '{backup_path}'")
            return None
        data = json.loads(backup_path.read_text(encoding="utf-8"))
        logger.info("System configuration restored from USB.")
        return data

    async def run_task_logic(self, task: Task) -> Dict[str, Any]:
        action = task.parameters.get("action")
        if action == "EXPORT_SKILL":
            skill_dict = task.parameters.get("skill")
            if skill_dict:
                skill = Skill(**skill_dict)
                pkg_path = self.export_skill_package(skill)
                return {"status": "EXPORTED", "path": str(pkg_path)}
        elif action == "IMPORT_SKILLS":
            loaded = self.load_skill_packages_from_usb()
            return {"status": "IMPORTED", "count": len(loaded), "skills": [s.model_dump() for s in loaded]}
        elif action == "BACKUP_CONFIG":
            cfg = task.parameters.get("config", {})
            bpath = self.backup_system_configuration(cfg)
            return {"status": "BACKED_UP", "path": str(bpath)}
        elif action == "RESTORE_CONFIG":
            restored = self.restore_system_configuration()
            return {"status": "RESTORED", "config": restored}

        return {"status": "COMPLETED", "node": self.name, "message": f"USB Agent processed '{task.title}'"}
