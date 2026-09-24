import pytest
import subprocess
from pathlib import Path


def test_inventory_and_version():
    inv_file = Path("config/GENX_FX_INVENTORY.yaml")
    assert inv_file.exists()
    content = inv_file.read_text(encoding="utf-8")
    assert "A6-9V" in content
    assert "LengKundee" in content
    assert "LENG-A6-9V-LAN-01" in content

    ver_file = Path("VERSION")
    assert ver_file.exists()
    assert "3.6.10" in ver_file.read_text(encoding="utf-8")


def test_one_loop_cli_commands():
    res_plan = subprocess.run(["./genx", "plan"], capture_output=True, text=True)
    assert res_plan.returncode == 0
    assert "JULES ONE-LOOP PLAN" in res_plan.stdout

    res_inv = subprocess.run(["./genx", "inventory"], capture_output=True, text=True)
    assert res_inv.returncode == 0
    assert "LENG-A6-9V-LAN-01" in res_inv.stdout

    res_deploy = subprocess.run(["./genx", "deploy"], capture_output=True, text=True)
    assert res_deploy.returncode == 0
    assert "DEPLOYMENT SUCCESSFUL" in res_deploy.stdout


def test_scripts_execution():
    res_health = subprocess.run(["./scripts/health.sh"], capture_output=True, text=True)
    assert res_health.returncode == 0
    assert "STATUS: HEALTHY" in res_health.stdout

    res_rollback = subprocess.run(["./scripts/rollback.sh"], capture_output=True, text=True)
    assert res_rollback.returncode == 0
    assert "STATUS: HEALTHY" in res_rollback.stdout
