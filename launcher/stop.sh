#!/usr/bin/env bash
set -euo pipefail

echo "Stopping GENX managed processes..."
pkill -f "src/main.py" 2>/dev/null || true
echo "GENX stopped."
