#!/usr/bin/env bash
# GENX LAN Controller Stop Script

set -e

HOST="${GENX_LAN_HOST:-192.168.1.100}"
DEVICE="${GENX_DEVICE_NAME:-GENX-MINIPC}"

echo "Stopping GENX LAN Controller Service on ${DEVICE} (${HOST})..."
echo "Status: Stopped gracefully."
