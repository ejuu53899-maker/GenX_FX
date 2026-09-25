import subprocess
from pathlib import Path


def run_cli_cmd(cmd_args: list[str]) -> subprocess.CompletedProcess:
    """Run ./genx CLI command with args."""
    return subprocess.run(["./genx"] + cmd_args, capture_output=True, text=True)


def test_cli_boot_and_monitor():
    res_boot = run_cli_cmd(["boot"])
    assert res_boot.returncode == 0
    assert "GENX READY" in res_boot.stdout

    res_mon = run_cli_cmd(["monitor"])
    assert res_mon.returncode == 0
    assert "GENX SYSTEM HEALTH DASHBOARD" in res_mon.stdout


def test_cli_device_commands():
    res_list = run_cli_cmd(["device", "list"])
    assert res_list.returncode == 0
    assert "GENX-MINIPC" in res_list.stdout

    res_conn = run_cli_cmd(["device", "connect", "MINIPC"])
    assert res_conn.returncode == 0
    assert "SSH Tunnel Established" in res_conn.stdout


def test_cli_ai_and_trade():
    res_ai = run_cli_cmd(["ai", "status"])
    assert res_ai.returncode == 0
    assert "Gemini MCP" in res_ai.stdout

    res_trade = run_cli_cmd(["trade", "status"])
    assert res_trade.returncode == 0
    assert "FxPro MT5" in res_trade.stdout

    res_stop = run_cli_cmd(["trade", "emergency-stop"])
    assert res_stop.returncode == 0
    assert "EMERGENCY STOP" in res_stop.stdout


def test_cli_container_storage_vault_network():
    res_cont = run_cli_cmd(["container", "list"])
    assert res_cont.returncode == 0
    assert "fastapi-bridge" in res_cont.stdout

    res_store = run_cli_cmd(["storage", "scan"])
    assert res_store.returncode == 0
    assert "BLUEDIM64GB" in res_store.stdout

    res_vault = run_cli_cmd(["vault", "status"])
    assert res_vault.returncode == 0
    assert "SECURE" in res_vault.stdout

    res_net = run_cli_cmd(["network", "scan"])
    assert res_net.returncode == 0
    assert "GENX LAN" in res_net.stdout


def test_cli_audit_log():
    run_cli_cmd(["device", "list"])
    audit_file = Path("data/logs/audit.json")
    assert audit_file.exists()
    content = audit_file.read_text(encoding="utf-8")
    assert "genx device list" in content
