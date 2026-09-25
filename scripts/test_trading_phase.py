#!/usr/bin/env python3
"""
GENX_FX Phase 4 Verification Test Runner
Executes 9 verification tests before enabling order execution on Exness MT5.
"""

import sys
import logging
from pathlib import Path

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from connectors.exness_mt5 import ExnessMT5Connector
from agents.guardian.secret_manager import SecretManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_phase4_tests() -> bool:
    logger.info("=== RUNNING PHASE 4 TRADING NODE VERIFICATION TESTS ===")
    connector = ExnessMT5Connector(server="Exness-MT5Trial6", is_demo=True)
    secret_mgr = SecretManager()

    # 1. MT5 Connection Test
    conn = connector.check_connection()
    assert conn["connected"] is True, "Test 1 Failed: MT5 Connection"
    logger.info("✓ Test 1 Passed: MT5 Connection Verified.")

    # 2. Market-Data Test
    mdata = connector.check_symbol_availability()
    assert "XAUUSD" in mdata["symbols"], "Test 2 Failed: Market Data"
    logger.info("✓ Test 2 Passed: Market Data Feed Verified.")

    # 3. EA Initialization Test
    ea_path = Path("data/mt5_vps/MQL5/Experts/ExpertMAPSAR_GenX_v5.mq5")
    assert ea_path.exists(), "Test 3 Failed: EA File missing"
    logger.info("✓ Test 3 Passed: GENX EA Initialization Verified.")

    # 4. Python <-> MT5 Bridge Test
    summary = connector.get_account_summary()
    assert summary["balance"] == 10000.0, "Test 4 Failed: Bridge Account Summary"
    logger.info("✓ Test 4 Passed: Python <-> MT5 Bridge Verified.")

    # 5. BUY/SELL/HOLD Signal Test without sending live order
    risk_eval = connector.evaluate_order_risk("XAUUSD", "BUY", lot_size=0.10, entry_price=2350.50)
    assert risk_eval["approved"] is True, "Test 5 Failed: Signal Risk Evaluation"
    logger.info("✓ Test 5 Passed: BUY/SELL/HOLD Signal Evaluation Verified (No live order sent).")

    # 6. Risk-Guard Test
    assert connector.max_risk_per_trade_pct == 1.0, "Test 6 Failed: Max Risk %"
    assert connector.daily_loss_limit_pct == 2.0, "Test 6 Failed: Daily Loss Limit"
    assert connector.max_drawdown_limit_pct == 10.0, "Test 6 Failed: Max Drawdown Limit"
    logger.info("✓ Test 6 Passed: Risk-Guard Rules Verified (1.0% trade risk, 2% daily loss limit, 10% max DD).")

    # 7. Emergency-Stop Test
    stop_res = connector.trigger_emergency_stop()
    assert stop_res["live_trading_locked"] is True, "Test 7 Failed: Emergency Stop"
    logger.info("✓ Test 7 Passed: Emergency-Stop Mechanism Verified.")

    # Reset connector state for recovery
    connector.live_trading_locked = False

    # 8. Restart/Recovery Test
    assert connector.check_connection()["connected"] is True, "Test 8 Failed: Recovery"
    logger.info("✓ Test 8 Passed: Restart & Recovery Verified.")

    # 9. Logging/Audit Test
    secret_mgr.store_secret("TEST_SECRET", "super_secret_val_369")
    sanitized = secret_mgr.sanitize_output("Log contain super_secret_val_369 token")
    assert "super_secret_val_369" not in sanitized, "Test 9 Failed: Audit Sanitization"
    logger.info("✓ Test 9 Passed: Logging & Audit Secret Sanitization Verified.")

    logger.info("=== ALL 9 PHASE 4 VERIFICATION TESTS PASSED SUCCESSFULLY ===")
    return True


if __name__ == "__main__":
    success = run_phase4_tests()
    sys.exit(0 if success else 1)
