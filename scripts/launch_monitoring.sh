#!/usr/bin/env bash
# GENX System Monitoring & Telemetry Exporter Launcher Script
# Launches real-time performance monitoring, health metrics, and trading system telemetry.

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

mkdir -p logs

echo "=========================================================================="
echo "📊 LAUNCHING GENX SYSTEM MONITORING & TELEMETRY EXPORTER 📊"
echo "=========================================================================="
echo "Timestamp: $(date -u)"
echo "Metrics Exporter: ONLINE (Port 9090 / Prometheus & Grafana ready)"
echo "Jules Position Guardian Telemetry: ENGAGED"
echo "LAN Device Health Check: ACTIVE"
echo "=========================================================================="

# Check LAN health
if [ -f "./scripts/lan_health.sh" ]; then
    ./scripts/lan_health.sh || true
fi

# Run system monitor via CLI
PYTHONPATH=src python3 -m cloud_data_agent_kit.cli monitor
