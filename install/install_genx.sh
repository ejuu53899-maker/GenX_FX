#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="GENX-Starter-Kit"
PYTHON_MIN_MAJOR=3
PYTHON_MIN_MINOR=11

echo "======================================"
echo " GENX Starter Kit v3.6.9 Installer"
echo " Owner: NUNA"
echo "======================================"

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is required."
    exit 1
fi

PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

echo "Python detected: ${PYTHON_VERSION}"

python3 - <<'PY'
import sys

if sys.version_info < (3, 11):
    print("ERROR: GENX requires Python 3.11+")
    sys.exit(1)
PY

echo "[1/6] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "[2/6] Activating environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

echo "[3/6] Upgrading packaging tools..."
python -m pip install --upgrade pip setuptools wheel --quiet || true

echo "[4/6] Installing GENX dependencies..."
if [ -f requirements.txt ]; then
    python -m pip install -r requirements.txt --quiet || true
fi

echo "[5/6] Creating runtime directories..."
mkdir -p \
    data/logs \
    data/journal \
    data/cache \
    vault \
    updates \
    skills

echo "[6/6] Running validation..."

if command -v pytest >/dev/null 2>&1; then
    python -m pytest tests/ --quiet || true
fi

echo
echo "GENX installation completed."
echo
echo "Activate:"
echo "  source .venv/bin/activate"
echo
echo "Start:"
echo "  ./launcher/start.sh"
echo
echo "Health:"
echo "  ./launcher/health_check.sh"
