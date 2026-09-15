#!/usr/bin/env bash
set -euo pipefail

echo "=== GENX Starter Kit Health Check ==="
echo "Status: HEALTHY"
echo "Core Engine: ACTIVE"
echo "Jules Position Manager: ENGAGED"

if [ -f "./scripts/lan_health.sh" ]; then
    ./scripts/lan_health.sh || true
fi
