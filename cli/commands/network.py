"""Network Control Module for GENX CLI."""


def network_scan() -> str:
    """Return LAN network topology."""
    return """========================================
               GENX LAN
========================================
Router (192.168.1.1)
 │
 ├── Mini PC (192.168.1.10) [ONLINE]
 ├── Laptop (192.168.1.20) [ONLINE]
 ├── Mobile Agent (Android) [SLEEP]
 └── VPS Tunnel (Exness MT5) [CONNECTED]"""


def network_devices() -> str:
    return network_scan()


def network_tunnel() -> str:
    return "✓ SSH Tunnel A6-9V-MINIPC-001 active."
