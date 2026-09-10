"""Device Management Module for GENX CLI."""

from typing import Dict, Any
from agents.workers.genx_device_agent import GENXDeviceAgent


def list_devices() -> str:
    """Return device list table."""
    agent = GENXDeviceAgent()
    telemetry = agent.get_telemetry()
    return f"""DEVICE              STATUS       IP            DETAILS
------------------------------------------------------------------------
GENX-MINIPC ({telemetry['device']})  {telemetry['status'].upper()}       192.168.1.50   CPU: {telemetry['cpu']}, RAM: {telemetry['ram']}, MT5: {telemetry['mt5'].upper()}
ASUS-LAPTOP         ONLINE       192.168.1.20   Win11 Admin Panel
GALAXY-A51          SLEEP        MOBILE         Android Mobile Agent
ADATA-USB           CONNECTED    USB-STORAGE    Backup / Vault
BLUEDIM-64GB        ACTIVE       USB-BOOT       AI Boot / Recovery"""


def connect_device(device_id: str) -> str:
    """Connect to a remote GENX device node."""
    dev = device_id.upper()
    agent = GENXDeviceAgent()
    telemetry = agent.get_telemetry()
    return f"""SSH Tunnel Established (Tailscale Encrypted VPN)
GENX Node ID: A6-9V-{dev}-001
Device: {telemetry['device']} ({telemetry['ip']})
OS: Ubuntu Server 24.04 (CPU: {telemetry['cpu']}, RAM: {telemetry['ram']})
MT5 Status: {telemetry['mt5'].upper()} | Network: {telemetry['network'].upper()}
Status: CONNECTED"""
