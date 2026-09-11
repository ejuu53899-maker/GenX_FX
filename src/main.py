#!/usr/bin/env python3
"""
GenX_FX Main Application v3.6.9
GENX AI Agent Center Handler / Central Nervous System Control Plane
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.agent_controller.orchestrator import AgentCenterHandlerController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/genx_fx.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class GenXFXApp:
    """Main application class for GenX_FX trading system v3.6.9"""

    def __init__(self):
        self.version = "3.6.9"
        self.name = "GENX Hybrid AI Agent Network"
        logger.info(f"Initializing {self.name} v{self.version}")
        self.controller = AgentCenterHandlerController()

    def start(self):
        """Start the GenX_FX application and AI Agent Center Handler Controller"""
        logger.info(f"Starting {self.name} v{self.version} Control Plane...")
        print(f"==================================================")
        print(f"🧠⚡ Welcome to {self.name} v{self.version}")
        print(f"Central Nervous System & AI Agent Operating System")
        print(f"==================================================")

        # Run sample mission & prompt diagnostic
        res = self.controller.process_command("Analyze XAUUSD market")
        print(f"\n[Command Dispatch Test] Result: {res['dispatch']['status']}")
        
        telemetry = self.controller.get_dashboard_telemetry()
        print(f"[Telemetry Overview] Agents Online: {len(telemetry['agents'])} | Devices: {telemetry['devices']['online_count']} | Skills: {telemetry['skills_loaded']}")
        print("\nSystem initialized successfully and listening for missions!")

    def stop(self):
        """Stop the GenX_FX application"""
        logger.info("Stopping GenX_FX Trading System...")
        print("GENX AI Agent Operating System shut down cleanly.")


def main():
    """Main entry point"""
    app = GenXFXApp()

    try:
        app.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        app.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
