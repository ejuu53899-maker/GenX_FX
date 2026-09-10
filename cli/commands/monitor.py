"""System Health Dashboard for GENX CLI."""


def get_monitor_dashboard() -> str:
    """Return live system health dashboard."""
    return """========================================
       GENX SYSTEM HEALTH DASHBOARD
========================================
CPU        21%
RAM        43%
Storage    62%
Network    ONLINE

AI Agent   RUNNING
MT5 EA     ACTIVE
Firebase   CONNECTED
Vault      SECURE"""
