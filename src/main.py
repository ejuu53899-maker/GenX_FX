#!/usr/bin/env python3
"""
GenX_FX Main Application - GENX 3.6.9 Agent Operating System
"""

import sys
import asyncio
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from agents.orchestrator import AgentOSOrchestrator

# Ensure logs directory exists
Path('logs').mkdir(exist_ok=True)

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
    """Main application class for GenX 3.6.9 Autonomous Device Intelligence Operating System"""

    def __init__(self):
        self.version = "3.6.9"
        self.name = "GenX_FX Agent Mode System"
        self.orchestrator = AgentOSOrchestrator()
        logger.info(f"Initializing {self.name} v{self.version}")

    async def start(self):
        """Start the GenX_FX application and agent startup sequence"""
        logger.info("Starting GenX_FX Agent Operating System...")
        print(f"Welcome to {self.name} v{self.version}")
        
        # Execute 7-step startup sequence
        success = await self.orchestrator.run_startup_sequence()
        if success:
            print("GENX 3.6.9 Agent OS initialized and running successfully!")
        else:
            print("GENX 3.6.9 Agent OS startup encountered warnings.")

    async def stop(self):
        """Stop the GenX_FX application"""
        logger.info("Stopping GenX_FX Trading System...")
        print("GenX_FX system stopped.")


def main():
    """Main entry point"""
    app = GenXFXApp()

    try:
        asyncio.run(app.start())
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        asyncio.run(app.stop())
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
