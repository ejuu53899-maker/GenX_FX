#!/usr/bin/env python3
"""
GenX_FX Main Application
A comprehensive trading system with AI-powered analysis, Skill Manager OS layer, and Agent Commander runtime.
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.skill_manager import SkillManager
from agents.commander.main import AgentCommander

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
    """Main application class for GenX_FX trading system"""

    def __init__(self):
        self.version = "3.6.9"
        self.name = "GENX 3.6.9 Device Ecosystem"
        self.skill_manager = SkillManager(root_dir=str(project_root))
        self.agent_commander = AgentCommander(skill_manager=self.skill_manager)
        logger.info(f"Initializing {self.name} v{self.version}")

    def start(self):
        """Start the GenX_FX application, skill ecosystem, and agent runtime"""
        logger.info("Starting GENX 3.6.9 Trading System & Skill OS...")
        print(f"Welcome to {self.name} v{self.version}")
        
        # Discover and initialize skill modules
        discovered = self.skill_manager.discover_skills()
        print(f"Skill OS Layer loaded: {len(discovered)} skills discovered.")

        # Run Agent Commander directive
        directive_result = self.agent_commander.execute_directive("Analyze trading market and record decision")
        print(f"Agent Commander Directive Status: {directive_result.get('status')}")
        print(f"Executed Steps: {len(directive_result.get('execution_results', []))}")

        print("System initialized successfully!")

    def stop(self):
        """Stop the GenX_FX application"""
        logger.info("Stopping GenX_FX Trading System...")
        print("GenX_FX system stopped.")


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
