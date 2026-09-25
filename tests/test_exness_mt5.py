import pytest
import subprocess
from pathlib import Path
from connectors.exness_mt5 import ExnessMT5Connector
from scripts.test_trading_phase import run_phase4_tests
from scripts.generate_deployment_report import generate_report


def test_exness_mt5_connector_risk_and_emergency():
    connector = ExnessMT5Connector(server="Exness-MT5Trial6", is_demo=True)
    conn_info = connector.check_connection()
    assert conn_info["connected"] is True
    assert conn_info["account_mode"] == "DEMO"

    summary = connector.get_account_summary()
    assert summary["balance"] == 10000.0

    symbols = connector.check_symbol_availability()
    assert "XAUUSD" in symbols["symbols"]

    # Evaluate order risk in DEMO
    risk_eval = connector.evaluate_order_risk("XAUUSD", "BUY", lot_size=0.10, entry_price=2350.50)
    assert risk_eval["approved"] is True

    # Test LIVE trading locked
    live_connector = ExnessMT5Connector(server="Exness-Real", is_demo=False)
    live_eval = live_connector.evaluate_order_risk("XAUUSD", "BUY", lot_size=0.10, entry_price=2350.50)
    assert live_eval["approved"] is False
    assert "LOCKED OFF" in live_eval["reason"]

    # Test emergency stop
    stop_res = connector.trigger_emergency_stop()
    assert stop_res["live_trading_locked"] is True


def test_phase4_tests_and_report_generation():
    passed = run_phase4_tests()
    assert passed is True

    report_path = generate_report()
    assert report_path.exists()
    content = report_path.read_text(encoding="utf-8")
    assert "Exness MT5" in content
    assert "LOCKED OFF" in content


def test_cli_deploy_exness_command():
    res_deploy = subprocess.run(["./genx", "trade", "deploy-exness"], capture_output=True, text=True)
    assert res_deploy.returncode == 0
    assert "EXNESS MT5 DEPLOYMENT SUCCESSFUL" in res_deploy.stdout

    res_rep = subprocess.run(["./genx", "trade", "report"], capture_output=True, text=True)
    assert res_rep.returncode == 0
    assert "EXNESS_DEPLOYMENT_REPORT" in res_rep.stdout or "Deployment Report" in res_rep.stdout
