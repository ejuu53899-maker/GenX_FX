#!/usr/bin/env bash
# AI Trading Data Merge & Sync Script
# Syncs attached runtime data files from /tmp/file_attachments/ai-trading-data into workspace

set -e

SOURCE_DIR="/tmp/file_attachments/ai-trading-data"
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Merging AI Trading Data from ${SOURCE_DIR} ==="

if [ -d "$SOURCE_DIR" ]; then
    mkdir -p "${TARGET_DIR}/data/market"
    mkdir -p "${TARGET_DIR}/data/features"
    mkdir -p "${TARGET_DIR}/state"
    mkdir -p "${TARGET_DIR}/backups/daily"
    mkdir -p "${TARGET_DIR}/logs"

    cp -rn "${SOURCE_DIR}/data/"* "${TARGET_DIR}/data/" 2>/dev/null || true
    cp -rn "${SOURCE_DIR}/state/"* "${TARGET_DIR}/state/" 2>/dev/null || true
    cp -rn "${SOURCE_DIR}/backups/"* "${TARGET_DIR}/backups/" 2>/dev/null || true
    echo "AI Trading Data successfully merged into workspace!"
else
    echo "Notice: Source attachment directory ${SOURCE_DIR} not found. Skipped."
fi
