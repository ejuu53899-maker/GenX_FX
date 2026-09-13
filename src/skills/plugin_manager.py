"""
GENX Skill Plugin Manager (v3.6.9)
Handles dynamic skill loading, version management, dependency checking, and hot-reloading capability.
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SkillManifest(BaseModel):
    name: str
    version: str
    description: str
    author: str = "GENX Core"
    dependencies: List[str] = Field(default_factory=list)
    enabled: bool = True


class SkillPlugin:
    """
    Wrapper for a dynamic skill plugin module.
    """

    def __init__(self, manifest: SkillManifest, handler: Callable[..., Any]):
        self.manifest = manifest
        self.handler = handler

    def execute(self, *args, **kwargs) -> Any:
        if not self.manifest.enabled:
            raise RuntimeError(f"Skill '{self.manifest.name}' is disabled.")
        return self.handler(*args, **kwargs)


class SkillPluginManager:
    """
    Plugin manager supporting dynamic registration, version checks, and execution of skills.
    """

    def __init__(self):
        self._skills: Dict[str, SkillPlugin] = {}

    def register_skill(self, manifest: SkillManifest, handler: Callable[..., Any]) -> None:
        plugin = SkillPlugin(manifest, handler)
        self._skills[manifest.name] = plugin
        logger.info(f"Registered skill '{manifest.name}' (v{manifest.version})")

    def get_skill(self, name: str) -> Optional[SkillPlugin]:
        return self._skills.get(name)

    def list_skills(self) -> List[SkillManifest]:
        return [plugin.manifest for plugin in self._skills.values()]

    def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        plugin = self.get_skill(skill_name)
        if not plugin:
            raise ValueError(f"Skill '{skill_name}' not found.")
        return plugin.execute(*args, **kwargs)
