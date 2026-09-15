#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo " Starting GENX Starter Kit v3.6.9"
echo "======================================"

python3 src/main.py --always-on "$@"
