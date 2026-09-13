"""
GENX AI Agent Center Handler Orchestrator v3.6.9
Central nervous system connecting Agent Router, Dispatcher, Three-Layer Memory,
Security Gatekeeper, Skill Plugin Manager, Device Network Controller, Mission Engine, and Trading Handler.
"""

import logging
from typing import Dict, List, Any, Optional
from src.agents.identity import AgentIdentity, AgentCard, PermissionLevel, AgentStatus
from src.core.agent_controller.router import AgentRouter
from src.core.agent_controller.dispatcher import AgentDispatcher
from src.memory.manager import ThreeLayerMemoryManager
from src.security.gatekeeper import SecurityGatekeeper
from src.skills.plugin_manager import SkillPluginManager, SkillManifest
from src.network.device_controller import DeviceNetworkController, DeviceTelemetry
from src.missions.mission_engine import MissionAutomationEngine, MissionDefinition, MissionStep
from src.core.trading_handler import TradingIntelligenceHandler, TradeSignal

logger = logging.getLogger(__name__)


class AgentCenterHandlerController:
    """
    GENX AI Agent Network Controller v3.6.9 - Central Nervous System.
    """

    def __init__(self):
        self.router = AgentRouter()
        self.dispatcher = AgentDispatcher(self.router)
        self.memory = ThreeLayerMemoryManager()
        self.security = SecurityGatekeeper()
        self.skills = SkillPluginManager()
        self.devices = DeviceNetworkController()
        self.missions = MissionAutomationEngine()
        self.trading = TradingIntelligenceHandler(self.security)

        self._initialize_default_agents()
        self._initialize_default_devices()
        self._initialize_default_skills()
        self._initialize_default_missions()

    def _initialize_default_agents(self) -> None:
        """Register default specialist agents into system."""
        agents = [
            AgentCard(
                identity=AgentIdentity(
                    agent_id="GENX-TRADER-001",
                    name="Trading AI",
                    role="Trading Intelligence Specialist",
                    permission_level=PermissionLevel.LEVEL_3_APPROVAL,
                    capabilities=["market_analysis", "signal_generation", "risk_assessment"],
                    tools=["mt5_connector", "market_data_api"]
                ),
                supported_intents=["market_analysis", "trade_execution"]
            ),
            AgentCard(
                identity=AgentIdentity(
                    agent_id="GENX-CODER-001",
                    name="Coding AI",
                    role="Software Engineering & System Builder",
                    permission_level=PermissionLevel.LEVEL_2_RECOMMEND,
                    capabilities=["code_generation", "bug_fixing", "refactoring"],
                    tools=["github_manager", "docker_manager"]
                ),
                supported_intents=["coding_task"]
            ),
            AgentCard(
                identity=AgentIdentity(
                    agent_id="GENX-SECURITY-001",
                    name="Security Guardian",
                    role="Security Gatekeeper & Secret Vault Guardian",
                    permission_level=PermissionLevel.LEVEL_4_AUTONOMOUS,
                    capabilities=["vault_management", "audit_logging", "threat_detection"],
                    tools=["vault_manager", "permission_checker"]
                ),
                supported_intents=["security_audit"]
            ),
            AgentCard(
                identity=AgentIdentity(
                    agent_id="GENX-DEVICE-001",
                    name="Device Network AI",
                    role="Edge Infrastructure Orchestrator",
                    permission_level=PermissionLevel.LEVEL_3_APPROVAL,
                    capabilities=["device_heartbeat", "telemetry", "remote_exec"],
                    tools=["ssh_bridge", "system_monitor"]
                ),
                supported_intents=["device_management", "mission_execution"]
            )
        ]

        for card in agents:
            self.router.register_agent(card)

    def _initialize_default_devices(self) -> None:
        """Register default nodes into device network."""
        self.devices.register_device(DeviceTelemetry(
            device_id="MINIPC-01", device_type="Mini PC", os="Ubuntu 22.04 LTS", cpu_percent=24.5, ram_percent=38.2
        ))
        self.devices.register_device(DeviceTelemetry(
            device_id="VPS-CONTABO-01", device_type="VPS", os="Ubuntu 24.04 LTS", cpu_percent=12.1, ram_percent=29.0
        ))
        self.devices.register_device(DeviceTelemetry(
            device_id="LAPTOP-DEV-01", device_type="Laptop", os="Windows 11 Pro", cpu_percent=45.0, ram_percent=52.0
        ))

    def _initialize_default_skills(self) -> None:
        """Register default core skill plugins."""
        self.skills.register_skill(
            SkillManifest(name="mt5_connector", version="2.1.0", description="MetaTrader 5 EA & Terminal Bridge"),
            handler=lambda symbol, action: f"Connected to MT5 for {symbol} {action}"
        )
        self.skills.register_skill(
            SkillManifest(name="telegram_control", version="1.0.0", description="Telegram Bot Alert System"),
            handler=lambda msg: f"Sent Telegram alert: {msg}"
        )

    def _initialize_default_missions(self) -> None:
        """Register default startup mission."""
        self.missions.register_mission(MissionDefinition(
            mission_id="START_GENX_TRADING",
            name="Start GENX Trading Mission",
            description="Automated startup mission connecting VPS, MT5, EA, and AI monitoring.",
            steps=[
                MissionStep(step_id="step_1", action="check_device", target="VPS-CONTABO-01"),
                MissionStep(step_id="step_2", action="start_service", target="MT5_Terminal"),
                MissionStep(step_id="step_3", action="enable_ai", target="GENX-TRADER-001"),
                MissionStep(step_id="step_4", action="send_alert", target="telegram_control")
            ],
            rollback_steps=[
                MissionStep(step_id="rb_1", action="stop_service", target="MT5_Terminal"),
                MissionStep(step_id="rb_2", action="send_alert", target="telegram_control")
            ]
        ))

    def process_command(self, user_command: str, session_id: str = "default_session", context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main entry point for handling user commands across the ecosystem.
        """
        logger.info(f"Processing user command: '{user_command}' [session={session_id}]")

        # 1. Record prompt into Working Memory
        self.memory.push_working_memory(session_id, key="user_prompt", content=user_command)

        # 2. Route command
        route_info = self.router.route_request(user_command, context)

        # 3. Dispatch execution
        dispatch_result = self.dispatcher.dispatch(route_info)

        # 4. Record decision in shared memory
        self.memory.record_shared_decision(
            key=f"command_{session_id}",
            decision={"command": user_command, "route": route_info, "result": dispatch_result},
            agent_ids=route_info.get("target_agent_ids", [])
        )

        return {
            "session_id": session_id,
            "route": route_info,
            "dispatch": dispatch_result,
            "telemetry": self.get_dashboard_telemetry()
        }

    def get_dashboard_telemetry(self) -> Dict[str, Any]:
        """
        Returns real-time system status and observability data for GENX Control Center Dashboard.
        """
        return {
            "version": "v3.6.9",
            "agents": [
                {
                    "agent_id": card.identity.agent_id,
                    "name": card.identity.name,
                    "status": card.identity.status,
                    "permission_level": card.identity.permission_level.name
                }
                for card in self.router.list_agents()
            ],
            "devices": self.devices.check_health(),
            "skills_loaded": len(self.skills.list_skills()),
            "audit_logs_count": len(self.security.get_audit_trail())
        }
