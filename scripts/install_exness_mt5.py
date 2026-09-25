#!/usr/bin/env python3
"""
GENX_FX Exness MT5 Terminal & EA Installer Script (Phase 2 & Phase 3)
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vault_core.vault_engine import VaultEngine
from connectors.exness_mt5 import ExnessMT5Connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("=== BEGINNING EXNESS MT5 & GENX_FX TRADING NODE DEPLOYMENT ===")

    # Phase 1: Discovery
    mt5_vps_dir = Path("data/mt5_vps")
    experts_dir = mt5_vps_dir / "MQL5" / "Experts"
    logs_dir = Path("logs")
    mt5_vps_dir.mkdir(parents=True, exist_ok=True)
    experts_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger.info("✓ Phase 1 Discovery: Dedicated MT5 VPS directory layout initialized.")

    # Phase 2: Exness MT5 EA Deployment
    ea_file = experts_dir / "ExpertMAPSAR_GenX_v5.mq5"
    ea_code = """//+------------------------------------------------------------------+
//|                                     ExpertMAPSAR_GenX_v5.mq5      |
//|               GENX 3.6.9 Smart EA Bridge for Exness MT5 Terminal |
//+------------------------------------------------------------------+
#property copyright "GENX Trading Intelligence System v3.6.9"
#property version   "5.00"

input string   InpBridgeHost = "http://127.0.0.1:8000"; // FastAPI Bridge
input double   InpMaxRiskPct = 1.0;                      // Max Risk %
input string   InpSymbol     = "XAUUSD";                 // Symbol

int OnInit() {
    Print("GENX Exness MT5 EA Bridge initialized in DEMO mode.");
    return(INIT_SUCCEEDED);
}
"""
    ea_file.write_text(ea_code, encoding="utf-8")
    logger.info(f"✓ Phase 2 Exness MT5: Deployed GENX EA Bridge at '{ea_file}'.")

    # Phase 3: Vault Security & Risk Config
    vault = VaultEngine()
    vault.store_secret("EXNESS_MT5_ACCOUNT", "12345678", owner="ExnessDeployment")
    vault.store_secret("EXNESS_SERVER", "Exness-MT5Trial6", owner="ExnessDeployment")

    connector = ExnessMT5Connector(server="Exness-MT5Trial6", is_demo=True)
    conn_info = connector.check_connection()
    summary = connector.get_account_summary()

    logger.info(f"✓ Phase 3 Security & Risk: Connected to {conn_info['server']} (Account {summary['account_number']}).")
    logger.info(f"✓ Account Mode: {summary['account_mode']} | LIVE Trading Locked: {connector.live_trading_locked}")
    logger.info("=== EXNESS MT5 & GENX_FX DEPLOYMENT INITIALIZED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
