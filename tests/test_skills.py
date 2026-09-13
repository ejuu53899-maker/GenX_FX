"""
Unit tests for Skill Plugin Manager.
"""

import pytest
from src.skills.plugin_manager import SkillPluginManager, SkillManifest


def test_skill_plugin_manager():
    manager = SkillPluginManager()
    manifest = SkillManifest(name="test_skill", version="1.0.0", description="Test skill description")

    manager.register_skill(manifest, handler=lambda x: x * 2)
    assert len(manager.list_skills()) == 1

    res = manager.execute_skill("test_skill", 21)
    assert res == 42
