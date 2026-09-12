#!/usr/bin/env bash
# One-Click Launcher for Jules Always-On Trading Positioning System Engine
# Ensures continuous real-time market positioning, symbol tracking, and profit-closing automation.

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================================================="
echo "🚀 STARTING JULES ALWAYS-ON TRADING POSITIONING SYSTEM ENGINE 🚀"
echo "=========================================================================="
echo "Status: ALWAYS-ON ACTIVE"
echo "Real-Time Market Symbol Manager: ENGAGED"
echo "Profit-Closing Trade Guardian: ENABLED"
echo "=========================================================================="

python3 src/main.py --always-on "$@"
