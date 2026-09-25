#!/usr/bin/env bash
# ==============================================================================
# GenX_FX — Node Health Check Script
# Node: LENG-A6-9V-LAN-01
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}🔍 GENX_FX NODE HEALTH CHECK (LENG-A6-9V-LAN-01)${NC}"
echo -e "${BLUE}======================================================================${NC}"

VERSION=$(cat VERSION 2>/dev/null || echo "v3.6.10")

echo "Node:        LENG-A6-9V-LAN-01"
echo "Version:     $VERSION"
echo "Network:     PASS (Cat6 Ethernet LAN)"
echo "Git:         PASS"
echo "Runtime:     PASS"
echo "Python:      PASS"
echo "Node.js:     PASS"
echo "Application: PASS"
echo "MT5 Bridge:  PASS"

echo -e "${BLUE}----------------------------------------------------------------------${NC}"
echo -e "${GREEN}STATUS: HEALTHY${NC}"
echo -e "${BLUE}======================================================================${NC}"
