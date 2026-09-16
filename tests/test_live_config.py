import json
import os
import yaml
from src.common.config_loader import ConfigLoader

def test_genx_live_config_yaml():
    config_path = "config/GENX_LIVE_CONFIG.yaml"
    assert os.path.exists(config_path)
    config = ConfigLoader.load_config(config_path)

    assert config.get("owner") == "NUNA"
    assert config.get("operator") == "Jules AI Agent"
    assert config.get("trading_mode") == "LIVE PRODUCTION"
    assert config.get("live_trading") is True

    rm = config.get("risk_management", {})
    assert rm.get("account_mode") == "LIVE"
    assert rm.get("risk_per_trade_pct_min") == 0.5
    assert rm.get("risk_per_trade_pct_max") == 1.0
    assert rm.get("max_daily_loss_pct") == 2.0
    assert rm.get("max_drawdown_pct") == 10.0

def test_risk_guard_json():
    rg_path = "config/risk_guard.json"
    assert os.path.exists(rg_path)
    with open(rg_path, 'r') as f:
        data = json.load(f)

    assert data.get("owner") == "NUNA"
    assert data.get("operator") == "Jules AI Agent"
    assert data.get("account_mode") == "LIVE"

    cp = data.get("capital_protection", {})
    assert cp.get("max_daily_loss_pct") == 2.0
    assert cp.get("max_drawdown_pct") == 10.0

    es = data.get("emergency_stop", {})
    assert es.get("command") == "JULES: EMERGENCY STOP"
    assert "STOP NEW ORDERS" in es.get("action_pipeline", [])

def test_jules_live_operator_md():
    md_path = "Jules_Live_Operator.md"
    assert os.path.exists(md_path)
    with open(md_path, 'r') as f:
        content = f.read()
    assert "JULES LIVE MODE CHECK" in content
    assert "ENABLE LIVE TRADING" in content
    assert "EMERGENCY STOP" in content

def test_skill_md():
    skill_path = "skills/genx-live-operator/SKILL.md"
    assert os.path.exists(skill_path)
    with open(skill_path, 'r') as f:
        content = f.read()
    assert content.startswith("---")
    parts = content.split("---", 2)
    assert len(parts) >= 3
    fm = yaml.safe_load(parts[1])
    assert fm.get("name") == "genx-live-operator"
    assert fm.get("license") == "Proprietary"
