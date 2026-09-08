# GENX 3.6.9 Agent OS Deployment Guide

## 🚀 One-Click Jules Deployment

Deploy and launch the complete GENX 3.6.9 Autonomous Device Intelligence Operating System with a single command:

```bash
./deploy.sh
```

Or via scripts path:

```bash
./scripts/deploy_jules.sh
```

---

## 🛠️ What One-Click Deployment Does

1. **Directories Initialization**: Creates required learning loop directories (`data/memories/`, `data/experiences/`, `data/failures/`, `data/improvements/`, `data/usb_drive/`, `logs/`).
2. **Environment & Dependency Checks**: Verifies Python 3.11+ environment.
3. **Diagnostic Verification**: Runs test suite to ensure all agents (Commander, Builder, DevOps, Trading, Guardian, Device Workers) are operational.
4. **Agent OS Launch**: Executes `src/main.py` initiating the 7-step startup sequence:
   - Security Agent (Guardian) starts
   - System Health Check
   - Commander Agent (Central Brain) starts
   - Skill loading
   - Device connection
   - Worker Agents (Mini PC, Laptop, USB Intelligence) initialization
   - Operations commencement

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
