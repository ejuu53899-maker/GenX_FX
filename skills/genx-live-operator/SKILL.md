---
name: genx-live-operator
description: Operations manual, risk management rules, live deployment script, and safety configuration for GENX Autonomous AI Trading Network v3.6.9 in Real Account Production Mode. Use when enabling live trading, configuring real account safety parameters, or performing emergency stops.
license: Proprietary
compatibility: Requires Contabo VPS 4 or Linux server with MetaTrader 5, Python 3.11+, and GENX_VAULT secrets setup
metadata:
  version: "3.6.9"
  owner: "NUNA"
  operator: "Jules AI Agent"
---

# GENX Autonomous AI Trading Network v3.6.9 - Live Operator Skill

## Overview

This skill defines the **Real Account Production Mode** operational protocols, risk guardrails, live deployment procedures, and emergency controls for the GENX Autonomous AI Trading Network v3.6.9.

- **Owner:** NUNA
- **Operator:** Jules AI Agent
- **Trading Mode:** LIVE PRODUCTION
- **Broker:** FxPro MT5 / Approved Broker Account
- **Infrastructure:** GENX VPS (Contabo VPS 4) + Mini PC + Mobile Control

---

## 🔴 LIVE TRADING ACTIVATION POLICY

Before Jules can enable real trading, all live verification gates must pass:

```
JULES LIVE MODE CHECK
        |
        ├── VPS Online ✅
        |
        ├── MT5 Connected ✅
        |
        ├── Broker Account Verified ✅
        |
        ├── EA Signature Verified ✅
        |
        ├── Risk Manager Active ✅
        |
        ├── Emergency Stop Tested ✅
        |
        └── LIVE MODE ENABLE
```

---

## 💰 Real Account Risk Configuration

Jules enforces strict capital protection boundaries:

- **Account Mode:** LIVE
- **Risk Per Trade:** 0.5% - 1.0%
- **Maximum Daily Loss:** 2.0%
- **Maximum Drawdown:** 10.0%
- **Maximum Open Positions:** Limited (Max 5 concurrent positions)
- **Lot Size:** Dynamic Risk Calculation

---

## 🧠 Jules Live Trading Role

Jules is **not** the trader. Jules is:
- ✅ **Risk supervisor**
- ✅ **Execution controller**
- ✅ **System monitor**
- ✅ **Strategy assistant**
- ✅ **Trade journal manager**

### Decision Pipeline

```
Market Data -> AI Analysis -> Risk Validation -> EA Execution -> Trade Journal
```

---

## 📡 Commands For Live Operation

### Enable Live Trading

```
JULES: ENABLE LIVE TRADING
```

**7-Step Process:**
1. Check VPS health
2. Connect MT5
3. Confirm broker server (FxPro-Real)
4. Load EA (`ExpertMAPSAR_GenX_v5_Portfolio_Risk_Manager`)
5. Check risk limits
6. Activate monitoring
7. Start execution

### Emergency Stop

```
JULES: EMERGENCY STOP
```

**Action Pipeline:**
```
STOP NEW ORDERS -> SAVE POSITIONS -> BACKUP DATA -> NOTIFY OWNER
```

---

## 📁 Key File References

- **Live Configuration:** `config/GENX_LIVE_CONFIG.yaml` (and root `GENX_LIVE_CONFIG.yaml`)
- **Risk Guard Engine:** `config/risk_guard.json` (and root `risk_guard.json`)
- **Operator Manual:** `Jules_Live_Operator.md`
- **VPS Deployment Script:** `scripts/install_genx_live.sh`
