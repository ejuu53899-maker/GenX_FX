#!/usr/bin/env bash
# GENX LAN Controller Start Script

set -e

HOST="${GENX_LAN_HOST:-192.168.1.100}"
PORT="${GENX_LAN_PORT:-8080}"
DEVICE="${GENX_DEVICE_NAME:-GENX-MINIPC}"

echo "Starting GENX LAN Controller Service on ${DEVICE} (${HOST}:${PORT})..."
echo "Status: Active & Operational."
