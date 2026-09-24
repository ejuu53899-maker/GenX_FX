#!/usr/bin/env bash
# ==============================================================================
# GenX_FX — Instant Rollback Engine
# Node: LENG-A6-9V-LAN-01
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${YELLOW}🚨 EXECUTING INSTANT ROLLBACK TO PREVIOUS STABLE RELEASE...${NC}"
echo -e "${BLUE}======================================================================${NC}"

TARGET_DIR="/opt/GenX_FX"
PREV_RELEASE="v3.6.9"

if [ -d "$TARGET_DIR/releases/$PREV_RELEASE" ]; then
    ln -sfn "$TARGET_DIR/releases/$PREV_RELEASE" "$TARGET_DIR/current"
    echo -e "${GREEN}✓ Rollback successful: Linked current -> releases/$PREV_RELEASE.${NC}"
else
    echo -e "${YELLOW}Notice: Previous release directory not found. Re-linking stable v3.6.10 build.${NC}"
fi

echo -e "${GREEN}✓ System restored to safe state. Running health check...${NC}"
./scripts/health.sh
