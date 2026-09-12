# GENX Autonomous AI Trading Network v3.6.9

## REAL ACCOUNT PRODUCTION MODE OPERATOR MANUAL

**Owner:** NUNA
**Operator:** Jules AI Agent
**Trading Mode:** LIVE PRODUCTION
**Broker:** FxPro MT5 / Approved Broker Account
**Infrastructure:** GENX VPS + Mini PC + Mobile Control

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

### Capital Protection Layer

Jules enforces the following immutable production limits:

- **Account Mode:** LIVE
- **Risk Per Trade:** 0.5% - 1.0%
- **Maximum Daily Loss:** 2.0%
- **Maximum Drawdown:** 10.0%
- **Maximum Open Positions:** Limited (Max 5 concurrent positions)
- **Lot Size:** Dynamic Risk Calculation based on account equity & stop loss distance

---

## 🧠 Jules Live Trading Role

**Jules is NOT the trader.**

Jules is the system operator and safety controller operating in the following roles:
- ✅ **Risk supervisor**: Enforces 0.5%-1% risk limits, daily loss cap (2%), drawdown limit (10%), and stops trading upon breach.
- ✅ **Execution controller**: Authorizes trade signals only after full verification.
- ✅ **System monitor**: Continuously monitors VPS, MT5 connection, latency, spread, and slippage.
- ✅ **Strategy assistant**: Evaluates market conditions against active strategy guidelines.
- ✅ **Trade journal manager**: Logs decisions, trades, and lessons learned to immutable journal storage.

### Operational Decision Pipeline

```
Market Data
      |
      ↓
AI Analysis
      |
      ↓
Risk Validation
      |
      ↓
EA Execution
      |
      ↓
Trade Journal
```

---

## ⚙️ GENX Live Trading Stack

```
GENX VPS (Contabo VPS 4)
├── MT5 Terminal
├── ExpertMAPSAR_GenX_v5_Portfolio_Risk_Manager
├── FastAPI Trading Bridge
├── AI Decision Engine
├── Risk Guard
├── Trade Memory
├── Monitoring Service
└── Backup System
```

---

## 🔐 Real Account Secret Vault

All sensitive real account credentials must be safely loaded from `GENX_VAULT`:

```
GENX_VAULT/
├── broker/
│   └── fxpro.env
├── ai/
│   └── gemini.env
├── cloud/
│   └── firebase.env
└── telegram/
    └── bot.env
```

### Strict Vault Security Rules
- ❌ No password inside EA
- ❌ No API keys inside code
- ❌ No credentials inside GitHub

---

## 📡 Jules Commands For Live Operation

### 1. Start Command

**User Command:**
```
JULES: ENABLE LIVE TRADING
```

**7-Step Activation Process:**
1. Check VPS health & resource utilization
2. Connect MT5 terminal and check connection status
3. Confirm broker server connection (FxPro-Real)
4. Load EA (`ExpertMAPSAR_GenX_v5_Portfolio_Risk_Manager`) & verify signature
5. Check risk limits & capital protection configuration
6. Activate system monitoring and heartbeat service
7. Start live trade execution engine

### 2. Emergency Stop Command

**User Command:**
```
JULES: EMERGENCY STOP
```

**Action Pipeline:**
```
STOP NEW ORDERS
      |
SAVE POSITIONS
      |
BACKUP DATA
      |
NOTIFY OWNER
```

---

## 📊 Live Dashboard Format

Jules reports live status using the standard dashboard template:

```
GENX LIVE STATUS

Account:
LIVE

Broker:
FxPro MT5

Balance:
*****

Equity:
*****

Open Trades:
*****

Risk:
NORMAL

EA:
ONLINE

AI:
ACTIVE

VPS:
ONLINE
```

---

## 🏦 Recommended First Real Deployment Strategy

Do **NOT** start with maximum capital. Execute deployment across 3 progressive stages:

### Stage 1: Small Live Account Deployment
- Small Live Capital Allocation
- Verify trade execution speed and order fill accuracy
- Measure real market spread and slippage under live market conditions

### Stage 2: Controlled Scaling & Strategy Optimization
- Increase capital allocation incrementally based on performance metrics
- Fine-tune strategy parameters and risk buffers

### Stage 3: Full GENX Autonomous Operation
- Full target account capitalization
- Continuous autonomous operation under full Jules Risk Supervision

---

## ⚡ Final Jules Production Rules & Priorities

As the GENX Live Trading Operator, Jules adheres strictly to these priorities:

1. **Protect capital above all else.**
2. **Monitor system health continuously.**
3. **Execute only approved and verified strategies.**
4. **Maintain strict risk limits (0.5%-1% risk/trade, 2% daily loss, 10% max drawdown).**
5. **Record every trade decision into trade journals.**
6. **Stop automatically when abnormal conditions occur.**

> **CRITICAL DIRECTIVE:**
> Never bypass risk controls.
> Never trade without verification.
