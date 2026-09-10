"""Device Management Module for GENX CLI."""

from typing import Dict, Any


def list_devices() -> str:
    """Return device list table."""
    return """DEVICE              STATUS       IP
----------------------------------------
GENX-MINIPC         ONLINE       192.168.1.10
ASUS-LAPTOP         ONLINE       192.168.1.20
GALAXY-A51          SLEEP        MOBILE
ADATA-USB           CONNECTED
BLUEDIM-64GB        ACTIVE"""


def connect_device(device_id: str) -> str:
    """Connect to a remote GENX device node."""
    dev = device_id.upper()
    return f"""SSH Tunnel Established
GENX Node ID: A6-9V-{dev}-001
Ubuntu Server 24.04 (CPU: N5105, RAM: 8GB)
Status: CONNECTED"""
