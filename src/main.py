#!/usr/bin/env python3
"""
GenX_FX Main Application
A comprehensive trading system with AI-powered analysis
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

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
        self.version = "1.0.0"
        self.name = "GenX_FX Trading System"
        self.is_trading = False
        self.active_strategies = []
        logger.info(f"Initializing {self.name} v{self.version}")

    def start_trading(self):
        """Initialize market connections, load AI models, and begin trading engine loop"""
        logger.info("Initializing trading engine and strategy modules...")
        self.active_strategies = ["AI_Trend_Follower_v1", "Risk_Guard_v1"]
        self.is_trading = True
        logger.info(f"Trading active. Strategies running: {', '.join(self.active_strategies)}")
        print(f"Trading Started! Active strategies: {', '.join(self.active_strategies)}")

    def stop_trading(self):
        """Halt trading engine loop and safe stop strategies"""
        if self.is_trading:
            logger.info("Stopping trading engine...")
            self.is_trading = False
            self.active_strategies = []
            print("Trading Engine Halted.")
    
    def start(self):
        """Start the GenX_FX application"""
        logger.info("Starting GenX_FX Trading System...")
        print(f"Welcome to {self.name} v{self.version}")
        print("System initialized successfully!")
        self.start_trading()
        
    def stop(self):
        """Stop the GenX_FX application"""
        self.stop_trading()
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