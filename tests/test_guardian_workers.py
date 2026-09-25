import pytest
from pathlib import Path
from agents.common.message_bus import MessageBus
from agents.common.schemas import PermissionLevel, Skill
from agents.guardian.guardian_agent import GuardianAgent
from agents.workers.mini_pc import MiniPCAgent
from agents.workers.laptop import LaptopAgent
from agents.workers.usb_intelligence import USBIntelligenceAgent


@pytest.mark.asyncio
async def test_guardian_secret_and_threat():
    bus = MessageBus()
    guardian = GuardianAgent(bus)

    guardian.secret_manager.store_secret("API_KEY", "super_secret_key_12345")
    sanitized = guardian.secret_manager.sanitize_output("Log output containing super_secret_key_12345 here.")
    assert "super_secret_key_12345" not in sanitized
    assert "***REDACTED***" in sanitized

    is_threat = guardian.threat_detection.evaluate_activity("TRADE_EXECUTION", {"lot_size": 100.0})
    assert is_threat is True


@pytest.mark.asyncio
async def test_device_workers(tmp_path: Path):
    bus = MessageBus()
    mini_pc = MiniPCAgent(bus)
    laptop = LaptopAgent(bus)
    usb_agent = USBIntelligenceAgent(bus, usb_mount_path=tmp_path / "usb")

    skill = Skill(
        skill_id="SKILL-001",
        name="LocalInferenceSkill",
        version="1.0.0",
        description="Local Llama inference skill",
    )

    pkg_file = usb_agent.export_skill_package(skill)
    assert pkg_file.exists()

    loaded_skills = usb_agent.load_skill_packages_from_usb()
    assert len(loaded_skills) == 1
    assert loaded_skills[0].name == "LocalInferenceSkill"

    # Backup & Restore config
    config = {"theme": "dark", "max_threads": 8}
    bpath = usb_agent.backup_system_configuration(config)
    assert bpath.exists()

    restored = usb_agent.restore_system_configuration()
    assert restored["max_threads"] == 8
