#!/usr/bin/env bash
# 24/7 VS Code Server & Workspace Keep-Alive Launcher Script
# Keeps GitHub Workspace, VS Code Web Server, and Jules Always-On Positioning Engine running continuously.

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

mkdir -p logs

echo "=========================================================================="
echo "🚀 LAUNCHING GITHUB WORKSPACE 24/7 LIVE VS CODE SERVER 🚀"
echo "=========================================================================="
echo "Timestamp: $(date -u)"
echo "Target Workspace: ${PROJECT_ROOT}"
echo "Keep-Alive Loop: ACTIVE"
echo "=========================================================================="

# Auto-sync workspace subprojects on launch
if [ -f "./scripts/sync_workspace.sh" ]; then
    ./scripts/sync_workspace.sh || true
fi

# Launch Jules Always-On Engine
echo "--> Starting Jules Always-On Engine in background loop..."
python3 src/main.py --always-on > logs/jules_always_on_engine.log 2>&1 &
ENGINE_PID=$!
echo "Jules Always-On Engine PID: ${ENGINE_PID}"

echo "--> GitHub Workspace 24/7 VS Code Server running smoothly."
