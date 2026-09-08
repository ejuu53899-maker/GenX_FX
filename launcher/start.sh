#!/usr/bin/env bash
set -e
echo "Starting GENX 3.6.9 Device Ecosystem..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/../src/main.py"
