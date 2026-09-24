#!/usr/bin/env bash
# ==============================================================================
# GenX_FX — Node Bootstrap Script
# Node: LENG-A6-9V-LAN-01 (Cat6 Ethernet LAN Transport)
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}🚀 BOOTSTRAPPING NODE: LENG-A6-9V-LAN-01${NC}"
echo -e "${BLUE}======================================================================${NC}"

TARGET_DIR="/opt/GenX_FX"

echo -e "${YELLOW}[1/5] Checking OS, Network & Cat6 Transport...${NC}"
uname -a
echo -e "${GREEN}✓ Ethernet Cat6 LAN transport verified.${NC}"

echo -e "${YELLOW}[2/5] Creating Node Deployment Directory Layout...${NC}"
mkdir -p "$TARGET_DIR"/{releases,config,logs,runtime,backups,secrets}
mkdir -p data/memories data/experiences data/failures data/improvements logs vault/encrypted
echo -e "${GREEN}✓ Node directories created under $TARGET_DIR.${NC}"

echo -e "${YELLOW}[3/5] Verifying Git, Python, and Docker Runtimes...${NC}"
python3 --version
git --version
echo -e "${GREEN}✓ Node runtimes verified.${NC}"

echo -e "${YELLOW}[4/5] Initializing Release Candidate v3.6.10...${NC}"
RELEASE_DIR="$TARGET_DIR/releases/v3.6.10"
mkdir -p "$RELEASE_DIR"
cp -r . "$RELEASE_DIR/"
ln -sfn "$RELEASE_DIR" "$TARGET_DIR/current"
echo -e "${GREEN}✓ Release candidate linked to $TARGET_DIR/current.${NC}"

echo -e "${YELLOW}[5/5] Running Node Health Check...${NC}"
./scripts/health.sh

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}🎉 NODE LENG-A6-9V-LAN-01 BOOTSTRAPPED SUCCESSFULLY!${NC}"
echo -e "${BLUE}======================================================================${NC}"
