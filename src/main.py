#!/usr/bin/env python3
"""
GenX_FX Main Application
A comprehensive trading system with AI-powered analysis
"""

import sys
import threading
import time
from pathlib import Path
import logging
import uvicorn

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.genx.engine import GenXEngine
from src.genz.engine import GenZEngine
from src.common.config_loader import ConfigLoader

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
    
    def __init__(self, config_file="config/default_config.yaml"):
        self.version = "1.0.0"
        self.name = "GenX_FX Trading System"
        logger.info(f"Initializing {self.name} v{self.version}")

        # Load configuration
        self.config = ConfigLoader.load_config(config_file)

        # Initialize Trading Engines with configuration
        self.genx_engine = GenXEngine(config=self.config)
        self.genz_engine = GenZEngine(config=self.config)

        self.running = False
    
    def _run_trading_loop(self):
        """Internal loop to periodically run the trading engines"""
        while self.running:
            try:
                # Run GenX Cycle
                self.genx_engine.run()

                # Run GenZ Cycle
                self.genz_engine.run()

                # Sleep for a interval (e.g., 60 seconds)
                time.sleep(60)
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                time.sleep(10)

    def start(self):
        """Start the GenX_FX application and API server"""
        logger.info("Starting GenX_FX Trading System...")
        print(f"Welcome to {self.name} v{self.version}")
        
        self.running = True

        # Start Trading Thread
        self.trading_thread = threading.Thread(target=self._run_trading_loop, daemon=True)
        self.trading_thread.start()

        # API Server Settings from config
        api_config = self.config.get('api_server', {})
        host = api_config.get('host', "0.0.0.0")
        port = api_config.get('port', 8000)

        # Start API Server in the main thread
        logger.info(f"Starting API Server on http://{host}:{port}")
        uvicorn.run("src.api.app:app", host=host, port=port, log_level="info")
        
    def stop(self):
        """Stop the GenX_FX application"""
        logger.info("Stopping GenX_FX Trading System...")
        self.running = False
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
