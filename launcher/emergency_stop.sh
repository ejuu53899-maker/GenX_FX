#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo " 🚨 EMERGENCY STOP INITIATED 🚨"
echo "======================================"

pkill -9 -f "python3" 2>/dev/null || true
echo "All GENX processes terminated immediately."
