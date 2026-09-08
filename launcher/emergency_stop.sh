#!/usr/bin/env bash
echo "Executing Emergency Stop on GENX 3.6.9 Device Ecosystem..."
pkill -f "python3.*src/main.py" || true
echo "All GENX services stopped."
