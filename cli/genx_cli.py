#!/usr/bin/env python3
"""
GENX CLI COMMAND CENTER v3.6.9
"One Command. Every Device. One AI Network."
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Add repo root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.commands import device, monitor, ai, trade, container, storage, vault, network, boot


def audit_log(command: str, result: str):
    """Write audit log record to data/logs/audit.json."""
    audit_file = Path("data/logs/audit.json")
    audit_file.parent.mkdir(parents=True, exist_ok=True)

    records = []
    if audit_file.exists():
        try:
            records = json.loads(audit_file.read_text(encoding="utf-8"))
        except Exception:
            records = []

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device": os.uname().nodename if hasattr(os, "uname") else "LOCAL",
        "command": command,
        "result": "SUCCESS" if "error" not in result.lower() else "FAILED",
    }
    records.append(record)
    audit_file.write_text(json.dumps(records, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        prog="genx",
        description="GENX CLI COMMAND CENTER v3.6.9 - Headless Command-Line Control Layer",
    )
    subparsers = parser.add_subparsers(dest="group", help="Available command groups")

    # genx status / genx boot / genx monitor
    subparsers.add_parser("status", help="Show system status summary")
    subparsers.add_parser("boot", help="Execute one-command system startup")
    subparsers.add_parser("monitor", help="Display system health dashboard")

    # genx device [list|connect|ssh]
    device_parser = subparsers.add_parser("device", help="Device Management")
    device_sub = device_parser.add_subparsers(dest="action")
    device_sub.add_parser("list")
    conn_p = device_sub.add_parser("connect")
    conn_p.add_argument("device_id", nargs="?", default="MINIPC")
    ssh_p = device_sub.add_parser("ssh")
    ssh_p.add_argument("device_id", nargs="?", default="MINIPC")

    # genx ai [status|start|stop|memory]
    ai_parser = subparsers.add_parser("ai", help="AI Agent Control")
    ai_sub = ai_parser.add_subparsers(dest="action")
    ai_sub.add_parser("status")
    ai_sub.add_parser("start")
    ai_sub.add_parser("stop")
    ai_sub.add_parser("memory")

    # genx trade [status|start|stop|emergency-stop|journal]
    trade_parser = subparsers.add_parser("trade", help="MT5 Trading Control")
    trade_sub = trade_parser.add_subparsers(dest="action")
    trade_sub.add_parser("status")
    trade_sub.add_parser("start")
    trade_sub.add_parser("stop")
    trade_sub.add_parser("emergency-stop")
    trade_sub.add_parser("journal")

    # genx container [list|restart]
    cont_parser = subparsers.add_parser("container", help="Docker Container Control")
    cont_sub = cont_parser.add_subparsers(dest="action")
    cont_sub.add_parser("list")
    restart_p = cont_sub.add_parser("restart")
    restart_p.add_argument("service_name", nargs="?", default="trade-ai")

    # genx storage [scan]
    storage_parser = subparsers.add_parser("storage", help="USB Device Management")
    storage_sub = storage_parser.add_subparsers(dest="action")
    storage_sub.add_parser("scan")

    # genx vault [status|rotate|backup|scan]
    vault_parser = subparsers.add_parser("vault", help="Secret Vault Control")
    vault_sub = vault_parser.add_subparsers(dest="action")
    vault_sub.add_parser("status")
    vault_sub.add_parser("rotate")
    vault_sub.add_parser("backup")
    vault_sub.add_parser("scan")

    # genx network [scan|devices|tunnel]
    net_parser = subparsers.add_parser("network", help="Network Control")
    net_sub = net_parser.add_subparsers(dest="action")
    net_sub.add_parser("scan")
    net_sub.add_parser("devices")
    net_sub.add_parser("tunnel")

    args = parser.parse_args()

    res = ""
    cmd_str = f"genx {args.group or ''} {getattr(args, 'action', '') or ''}".strip()

    if args.group == "status" or args.group == "monitor":
        res = monitor.get_monitor_dashboard()
    elif args.group == "boot":
        res = boot.boot_system()

    elif args.group == "device":
        if args.action == "connect" or args.action == "ssh":
            res = device.connect_device(getattr(args, "device_id", "MINIPC"))
        else:
            res = device.list_devices()

    elif args.group == "ai":
        if args.action == "start":
            res = ai.ai_start()
        elif args.action == "stop":
            res = ai.ai_stop()
        elif args.action == "memory":
            res = ai.ai_memory()
        else:
            res = ai.ai_status()

    elif args.group == "trade":
        if args.action == "start":
            res = trade.trade_start()
        elif args.action == "stop":
            res = trade.trade_stop()
        elif args.action == "emergency-stop":
            res = trade.trade_emergency_stop()
        elif args.action == "journal":
            res = trade.trade_journal()
        else:
            res = trade.trade_status()

    elif args.group == "container":
        if args.action == "restart":
            res = container.restart_container(getattr(args, "service_name", "trade-ai"))
        else:
            res = container.list_containers()

    elif args.group == "storage":
        res = storage.scan_storage()

    elif args.group == "vault":
        if args.action == "rotate":
            res = vault.vault_rotate()
        elif args.action == "backup":
            res = vault.vault_backup()
        elif args.action == "scan":
            res = vault.vault_scan()
        else:
            res = vault.vault_status()

    elif args.group == "network":
        if args.action == "tunnel":
            res = network.network_tunnel()
        else:
            res = network.network_scan()

    else:
        parser.print_help()
        sys.exit(0)

    print(res)
    audit_log(cmd_str, res)


if __name__ == "__main__":
    main()
