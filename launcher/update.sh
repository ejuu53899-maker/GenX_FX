#!/usr/bin/env bash
set -euo pipefail

echo "=== Updating GENX Starter Kit ==="
if [ -f "./scripts/sync_workspace.sh" ]; then
    ./scripts/sync_workspace.sh
fi
echo "GENX update complete."
