#!/usr/bin/env python3
"""
GenX_FX Main Application
A comprehensive trading system with AI-powered analysis, Google Cloud Data Agent Kit,
and Jules Always-On Trading Positioning System Engine.
"""

import sys
import argparse
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from cloud_data_agent_kit.config import DataAgentKitConfig
from cloud_data_agent_kit.agents import DataAnalystAgent, DataPipelineAgent, DataQualityAgent, DataGovernanceAgent
from trading.jules_position_manager import JulesPositionManager, OpenPosition

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
    """Main application class for GenX_FX trading system with Jules Always-On Engine integration."""
    
    def __init__(self, always_on: bool = False):
        self.version = "1.0.0"
        self.name = "GenX_FX Trading System"
        self.always_on = always_on
        logger.info(f"Initializing {self.name} v{self.version}")

        # Initialize Google Cloud Data Agent Kit
        self.data_agent_config = DataAgentKitConfig()
        self.data_analyst = DataAnalystAgent(self.data_agent_config)
        self.data_pipeline = DataPipelineAgent(self.data_agent_config)
        self.data_quality = DataQualityAgent(self.data_agent_config)
        self.data_governance = DataGovernanceAgent(self.data_agent_config)

        # Initialize Jules Real-Time Position Manager Engine
        self.position_manager = JulesPositionManager()
        logger.info("Jules Always-On Positioning System Engine Initialized.")
    
    def start(self):
        """Start the GenX_FX application and real-time position manager engine."""
        logger.info("Starting GenX_FX Trading System...")
        print(f"Welcome to {self.name} v{self.version}")
        print("System initialized successfully!")
        print("Google Cloud Data Agent Kit (Starter Pack) Active.")
        print("Jules Always-On Positioning Engine: RUNNING")

        # Pre-populate sample market open positions if running in always-on mode
        if self.always_on:
            print("\n==========================================================================")
            print("🚀 JULES ALWAYS-ON TRADING POSITIONING SYSTEM ENGINE ACTIVE 🚀")
            print("Rule Enforced: Jules must manage closing all active symbol trades with profit.")
            print("==========================================================================\n")

            sample_positions = [
                OpenPosition(ticket_id="1001", symbol="EURUSD", order_type="BUY", open_price=1.0840, current_price=1.0855, volume=0.1, floating_profit=15.00),
                OpenPosition(ticket_id="1002", symbol="BTCUSD", order_type="BUY", open_price=62000.0, current_price=62400.0, volume=0.05, floating_profit=20.00),
                OpenPosition(ticket_id="1003", symbol="GBPUSD", order_type="SELL", open_price=1.2950, current_price=1.2920, volume=0.1, floating_profit=30.00),
            ]
            for pos in sample_positions:
                self.position_manager.register_open_position(pos)

            # Execute real-time position management and profit-closing evaluation
            closing_actions = self.position_manager.evaluate_and_manage_positions()
            print(f"Managed {len(closing_actions)} trades closing with profit:")
            for action in closing_actions:
                print(f"  - Closed Ticket #{action['ticket_id']} ({action['symbol']}) with +${action['realized_profit']:.2f} profit")

            status = self.position_manager.get_system_status()
            print(f"\nTotal Realized Profit: +${status['total_realized_profit_usd']:.2f}")
        
    def stop(self):
        """Stop the GenX_FX application"""
        logger.info("Stopping GenX_FX Trading System...")
        print("GenX_FX system stopped.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="GenX_FX Trading System & Jules Engine")
    parser.add_argument("--always-on", action="store_true", help="Run Jules Always-On Positioning System Engine")
    args = parser.parse_args()

    app = GenXFXApp(always_on=args.always_on)
    
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
