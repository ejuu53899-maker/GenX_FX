# 🚀 Deployment Index

Deployment workflows, Jules One-Loop Deployment, node bootstrap, Contabo VPS cloud installer, MT5 VPS installer, and startup/shutdown procedures.

## ⚡ One-Click Deployment Commands

### Jules One-Loop Deployment
```bash
./genx deploy
```

### Node Bootstrap (LENG-A6-9V-LAN-01 Cat6 Ethernet Node)
```bash
./scripts/bootstrap.sh
```

### Contabo VPS Cloud Brain Deployment (Ubuntu Server 24.04)
```bash
./scripts/contabo_deploy.sh
```

### MT5 VPS & EA Private Hosting Installer (Ubuntu/Windows VPS)
```bash
./scripts/install_mt5_ea.sh
```

### Node Health Check & Rollback Commands
```bash
./scripts/health.sh
./scripts/rollback.sh
```

## 🔄 Startup Sequence (Executed via `src/main.py` / `AgentOSOrchestrator`)

1. **Step 1**: Security Agent (Guardian) starts
2. **Step 2**: System Health Check & Backup Verification
3. **Step 3**: Commander Agent (Central Brain) starts
4. **Step 4**: Skill Loading & Capabilities Import
5. **Step 5**: Connecting Devices & Device Nodes
6. **Step 6**: Starting Device Worker Agents (Mini PC, Laptop, USB Intelligence)
7. **Step 7**: Operations Commencement

## 🛑 Shutdown Command

```bash
Ctrl+C
```
(Triggers graceful shutdown handler in `src/main.py`)
