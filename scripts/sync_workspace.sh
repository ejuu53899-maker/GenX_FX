#!/usr/bin/env bash
# Continuous Workspace Syncing Script for GenX_FX Monorepo
set -e

SOURCE_DIR="${SYNC_SOURCE:-/tmp/file_attachments/Workspace-Monorepo-main}"
TARGET_DIR="${WORKSPACE_DIR:-/app}"

echo "=== Syncing Workspace Monorepo Changes ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Warning: Source directory $SOURCE_DIR does not exist. Skipping rsync."
    exit 0
fi

# Sync files while avoiding overwriting .git or root configs unless updated
rsync -av --update \
    --exclude='.git' \
    --exclude='.env*' \
    "$SOURCE_DIR/" "$TARGET_DIR/"

echo "Workspace sync complete at $(date)"
