# GENX 3.6.9 Agent OS Deployment Guide

## 🚀 GenX_FX — Jules One-Loop Deployment

Execute the complete Jules One-Loop Deployment pipeline (`genx deploy`):

```bash
./genx deploy
```

Or run bootstrap on node `LENG-A6-9V-LAN-01`:

```bash
./scripts/bootstrap.sh
```

---

## 📈 Exness MT5 Windows & Linux Trading Node Deployment

Deploy Exness MT5, install `ExpertMAPSAR_GenX_v5.mq5` EA bridge, run Phase 4 verification tests, and generate `EXNESS_DEPLOYMENT_REPORT.md`:

```bash
./genx trade deploy-exness
```

Or via direct scripts:

```bash
# Linux Node / Wine:
python3 scripts/install_exness_mt5.py
python3 scripts/test_trading_phase.py
python3 scripts/generate_deployment_report.py

# Windows Node (PowerShell):
powershell -ExecutionPolicy Bypass -File scripts/install_exness_mt5_win.ps1
```

### 🔒 Exness Risk & Safety Controls
- **Account Mode:** `DEMO` by default
- **LIVE Trading Gate:** 🛑 `LOCKED OFF` (Requires explicit owner review & authorization)
- **Max Risk per Trade:** 0.5 – 1.0%
- **Daily Loss Limit:** 2.0%
- **Max Drawdown Cap:** 10.0%
- **Emergency Stop:** Closing automated trading upon trigger

---

## 🔄 The Jules One-Loop Deployment Flow

```
JULES (Orchestrator) ──► PLAN ──► DISCOVER ──► BACKUP ──► GIT ──► CI ──► VERIFY
                                                                          │
                                                                          ▼
RUNNING ◄── PASS ── HEALTH ◄── DEPLOY ◄── LENG-A6-9V ◄── CAT6 ◄── RELEASE ◄── BUILD
   │                  │
   ▼                  │
MONITOR ──► UPDATE ───┘
   │
   └── FAIL ──► ROLLBACK ──► PREVIOUS STABLE
```

1. **Jules Orchestrates**: `Jules` plans, verifies, deploys, and monitors.
2. **Git Records**: Source of truth is `git@github.com:A6-9V/GenX_FX.git`.
3. **CI Verifies**: GitHub Actions runs dependency, secret scan, python & MT5 checks.
4. **Cat6 LAN Node Executes**: Cat6 transport deploys release candidate to node `LENG-A6-9V-LAN-01` (`/opt/GenX_FX/`).
5. **Trading Safety Gate**: Application deployment defaults to `TRADING = DISABLED`. Trading requires explicit risk and owner authorization before live MT5 enablement.
6. **Health System Decides**: Health check (`./scripts/health.sh`) promotes or triggers automatic rollback (`./scripts/rollback.sh`).

---

## ☁️ Contabo VPS Cloud Brain Deployment (3-Node Network)

Deploy the GENX Cloud Server on Contabo VPS (Ubuntu Server 24.04, 4 vCPU / 8GB RAM) with Docker, Tailscale, UFW security policy, and Risk Engine limits (0.5–1% risk/trade, 2% daily cap):

```bash
./scripts/contabo_deploy.sh
```

### 🌐 3-Node Network Topology
- **Contabo VPS** (`192.168.1.100`): Cloud Control & Risk Engine Server
- **GK3PRO Mini PC / LENG-A6-9V-LAN-01** (`192.168.1.50`): Local Execution & Trading Worker
- **Huawei Mobile** (`Android`): Mobile Monitor & Emergency Control

---

## 💻 Manual Launch

If preferred, you can run the application directly:

```bash
python3 src/main.py
```

## 🧪 Testing

Run full test suite:

```bash
python3 -m pytest
```
