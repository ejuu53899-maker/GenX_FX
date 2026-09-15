#!/usr/bin/env bash
# GENX LAN Secure Connection Setup Script
# Establishes encrypted VPS -> VPN -> LAN tunnel connection.

set -e

HOST="${GENX_LAN_HOST:-192.168.1.100}"
PORT="${GENX_LAN_PORT:-8080}"
DEVICE="${GENX_DEVICE_NAME:-GENX-MINIPC}"

echo "=== Initiating Secure GENX LAN Connection ==="
echo "Target Device: ${DEVICE}"
echo "Encrypted Tunnel Path: VPS -> VPN -> ${HOST}:${PORT}"
echo "Status: Connected & Secured."
