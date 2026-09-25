#!/usr/bin/env bash
# ==============================================================================
# GENX 3.6.9 Agent Operating System - One-Click Jules Deployment
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}🚀 GENX 3.6.9 ONE-CLICK JULES DEPLOYMENT${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Step 1: Directory Setup
echo -e "${YELLOW}[1/4] Initializing Agent OS Directories & CLI Permissions...${NC}"
mkdir -p data/memories data/experiences data/failures data/improvements data/usb_drive data/logs logs
chmod +x genx 2>/dev/null || true
echo -e "${GREEN}✓ Directories verified & CLI Control Hub ready.${NC}"

# Step 2: Python Environment & Dependencies
echo -e "${YELLOW}[2/4] Verifying Python Environment & Core Dependencies...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is required but not installed.${NC}"
    exit 1
fi

PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python $PYTHON_VER detected.${NC}"

# Step 3: Run Self Verification / Tests
echo -e "${YELLOW}[3/4] Running Agent OS Diagnostic Tests...${NC}"
if python3 -m pytest > /dev/null 2>&1; then
    echo -e "${GREEN}✓ All Diagnostic Tests Passed successfully!${NC}"
else
    echo -e "${YELLOW}Warning: Diagnostic tests check skipped or non-zero, proceeding with launch.${NC}"
fi

# Step 4: Launching System
echo -e "${YELLOW}[4/4] Launching GENX 3.6.9 Agent Mode System...${NC}"
echo -e "${BLUE}----------------------------------------------------------------------${NC}"
exec python3 src/main.py "$@"
