#!/usr/bin/env bash
set -euo pipefail

EXTENSION="${1:-}"

if [ -z "$EXTENSION" ]; then
    echo "Usage:"
    echo "  ./scripts/install_extension.sh <extension-path>"
    exit 1
fi

if [ ! -d "$EXTENSION" ]; then
    echo "ERROR: Extension directory not found: $EXTENSION"
    exit 1
fi

MANIFEST="$EXTENSION/manifest.yaml"

if [ ! -f "$MANIFEST" ]; then
    echo "ERROR: manifest.yaml not found in $EXTENSION"
    exit 1
fi

echo "======================================"
echo " GENX Extension Installer v3.6.9"
echo "======================================"
echo "Extension Path: $EXTENSION"

NAME="$(basename "$EXTENSION")"
TARGET="skills/$NAME"

mkdir -p skills

if [ -e "$TARGET" ]; then
    echo "ERROR: Extension already exists at $TARGET"
    exit 1
fi

echo "Validating extension structure..."

required_files=(
    "manifest.yaml"
    "README.md"
    "src"
    "tests"
    "version.txt"
)

for item in "${required_files[@]}"; do
    if [ ! -e "$EXTENSION/$item" ]; then
        echo "ERROR: Missing required extension component: $item"
        exit 1
    fi
done

echo "Installing extension into $TARGET..."
cp -R "$EXTENSION" "$TARGET"

echo
echo "Extension installed successfully:"
echo "  $TARGET"
echo
echo "Next:"
echo "  ./launcher/health_check.sh"
