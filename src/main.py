#!/usr/bin/env python3
"""
GenX_FX Main Application
A comprehensive trading system with AI-powered analysis and Google Cloud Data Agent Kit
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from cloud_data_agent_kit.config import DataAgentKitConfig
from cloud_data_agent_kit.agents import DataAnalystAgent, DataPipelineAgent, DataQualityAgent, DataGovernanceAgent

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
    """Main application class for GenX_FX trading system with Google Cloud Data Agent Kit integration"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.name = "GenX_FX Trading System"
        logger.info(f"Initializing {self.name} v{self.version}")

        # Initialize Google Cloud Data Agent Kit
        self.data_agent_config = DataAgentKitConfig()
        self.data_analyst = DataAnalystAgent(self.data_agent_config)
        self.data_pipeline = DataPipelineAgent(self.data_agent_config)
        self.data_quality = DataQualityAgent(self.data_agent_config)
        self.data_governance = DataGovernanceAgent(self.data_agent_config)
        logger.info("Google Cloud Data Agent Kit initialized successfully.")
    
    def start(self):
        """Start the GenX_FX application"""
        logger.info("Starting GenX_FX Trading System...")
        print(f"Welcome to {self.name} v{self.version}")
        print("System initialized successfully!")
        print("Google Cloud Data Agent Kit (Starter Pack) Active.")
        
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
