#!/usr/bin/env bash
# Workspace Sync Script for Monorepo & Subprojects
# Synchronizes JetBrainsMono, ZOLO-A6-9VxNUNA-, and additional sub-repositories.

set -e

echo "=== Syncing Monorepo Workspace Subprojects ==="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Sync ZOLO-A6-9VxNUNA-
if [ -d "ZOLO-A6-9VxNUNA-" ]; then
    echo "--> Syncing ZOLO-A6-9VxNUNA-..."
    (cd ZOLO-A6-9VxNUNA- && git fetch origin && git checkout main && git merge origin/main --no-edit || true)
else
    echo "--> Cloning ZOLO-A6-9VxNUNA-..."
    git clone https://github.com/L6-N9/ZOLO-A6-9VxNUNA-.git ZOLO-A6-9VxNUNA-
fi

# Sync JetBrainsMono
if [ -d "JetBrainsMono" ]; then
    echo "--> Syncing JetBrainsMono..."
    (cd JetBrainsMono && git fetch origin && git checkout master 2>/dev/null || git checkout main 2>/dev/null || true)
else
    echo "--> Cloning JetBrainsMono..."
    git clone https://github.com/JetBrains/JetBrainsMono.git JetBrainsMono
fi

echo "=== Monorepo Workspace Sync Completed Successfully ==="
