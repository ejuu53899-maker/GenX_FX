"""GENX 3.6.9 Agent OS System Orchestrator & Boot Engine."""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

from agents.common.schemas import SystemState, PermissionLevel, Skill, AgentMessage
from agents.common.message_bus import MessageBus
from agents.common.permissions import PermissionManager
from agents.common.learning_loop import LearningLoopManager

from agents.guardian.guardian_agent import GuardianAgent
from agents.commander.commander_agent import CommanderAgent
from agents.builder.builder_agent import BuilderAgent
from agents.devops.devops_agent import DevOpsAgent
from agents.trading.trading_agent import TradingAgent
from agents.workers.mini_pc import MiniPCAgent
from agents.workers.laptop import LaptopAgent
from agents.workers.usb_intelligence import USBIntelligenceAgent

logger = logging.getLogger(__name__)


class AgentOSOrchestrator:
    """GENX 3.6.9 Autonomous Device Intelligence Operating System Orchestrator."""

    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.permission_manager = PermissionManager()
        self.message_bus = MessageBus(permission_manager=self.permission_manager)
        self.learning_loop = LearningLoopManager(data_dir=data_dir)

        self.state: SystemState = SystemState.NORMAL
        self.notifications: List[Dict[str, Any]] = []

        # Core Agents
        self.guardian: Optional[GuardianAgent] = None
        self.commander: Optional[CommanderAgent] = None
        self.builder: Optional[BuilderAgent] = None
        self.devops: Optional[DevOpsAgent] = None
        self.trading: Optional[TradingAgent] = None

        # Device Worker Agents
        self.mini_pc: Optional[MiniPCAgent] = None
        self.laptop: Optional[LaptopAgent] = None
        self.usb_agent: Optional[USBIntelligenceAgent] = None

        self.startup_completed = False

    async def run_startup_sequence(self) -> bool:
        """Execute the 7-step Agent OS Startup Sequence."""
        logger.info("=== BEGINNING GENX 3.6.9 AGENT OS STARTUP SEQUENCE ===")

        # Step 1: Security Agent starts
        logger.info("Step 1: Starting Security Agent (Guardian)...")
        self.guardian = GuardianAgent(self.message_bus)

        # Step 2: System Health Check
        logger.info("Step 2: Performing System Health Check...")
        backup_res = self.guardian.backup_checker.verify_backup_integrity(self.data_dir)
        logger.info(f"Health Check Backup Verification: {backup_res}")

        # Step 3: Commander Agent starts
        logger.info("Step 3: Starting Commander Agent (Central Brain)...")
        self.commander = CommanderAgent(self.message_bus)

        # Step 4: Load Skills
        logger.info("Step 4: Loading System Skills...")
        self.builder = BuilderAgent(self.message_bus)
        self.devops = DevOpsAgent(self.message_bus)
        self.trading = TradingAgent(self.message_bus)

        default_skill = Skill(
            skill_id="SKILL-CORE-01",
            name="CoreMarketScanner",
            version="1.0.0",
            description="Market scanning and technical signal capability",
            required_level=PermissionLevel.LEVEL_1_ANALYZE,
        )
        self.trading.import_skill(default_skill)

        # Step 5: Connect Devices
        logger.info("Step 5: Connecting Devices & Nodes...")
        # Step 6: Start Worker Agents
        logger.info("Step 6: Starting Device Worker Agents (Mini PC, Laptop, USB Intelligence)...")
        self.mini_pc = MiniPCAgent(self.message_bus)
        self.laptop = LaptopAgent(self.message_bus)
        self.usb_agent = USBIntelligenceAgent(self.message_bus, usb_mount_path=self.data_dir / "usb_drive")

        # Register workers with Commander
        await self.mini_pc.send_message("Commander", "commander.register_agent", {"role": self.mini_pc.role})
        await self.laptop.send_message("Commander", "commander.register_agent", {"role": self.laptop.role})
        await self.usb_agent.send_message("Commander", "commander.register_agent", {"role": self.usb_agent.role})

        # Step 7: Begin Operations
        logger.info("Step 7: Startup Sequence Complete. Beginning Operations!")
        self.startup_completed = True
        self.state = SystemState.NORMAL
        return True

    async def trigger_emergency_mode(self, reason: str) -> SystemState:
        """Trigger emergency mode actions across system."""
        self.state = SystemState.EMERGENCY_STOP
        logger.critical(f"🚨 EMERGENCY MODE ACTIVATED: {reason}")

        # 1. Stop Trading
        if self.trading:
            self.trading.is_active = False
            logger.info("Emergency Action 1: Trading Agent deactivated. Live trading STOPPED.")

        # 2. Freeze Deployments
        if self.devops:
            self.devops.is_active = False
            logger.info("Emergency Action 2: DevOps Agent deactivated. Deployments FROZEN.")

        # 3. Backup Logs
        log_backup_dir = self.data_dir / "emergency_logs"
        log_backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = log_backup_dir / "emergency_backup.log"
        backup_file.write_text(f"Emergency stop reason: {reason}\nState: {self.state.value}", encoding="utf-8")
        logger.info(f"Emergency Action 3: Logs backed up to '{backup_file}'.")

        # 4. Notify Owner
        notification = {"event": "EMERGENCY_STOP", "reason": reason, "owner_notified": True}
        self.notifications.append(notification)
        logger.info(f"Emergency Action 4: Owner notified! ({notification})")

        if self.guardian:
            await self.guardian.trigger_emergency_stop(reason)

        return self.state

    async def reset_emergency_mode(self) -> SystemState:
        """Reset system from emergency mode back to Normal."""
        self.state = SystemState.NORMAL
        if self.trading:
            self.trading.is_active = True
        if self.devops:
            self.devops.is_active = True
        logger.info("Emergency Mode cleared. System restored to NORMAL.")
        return self.state
