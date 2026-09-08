# GenX_FX Trading System - GENX 3.6.9 Agent OS

A comprehensive AI-powered foreign exchange trading system and Autonomous Device Intelligence Operating System.

## 🚀 One-Click Jules Deployment

Deploy and launch the complete GENX 3.6.9 Agent Mode Operating System with a single command:

```bash
./deploy.sh
```

or:

```bash
./scripts/deploy_jules.sh
```

For complete deployment details, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🤖 GENX 3.6.9 Agent Architecture

- **🧠 Commander Agent** (`agents/commander/`): Central Brain (Planner, Decision Engine, Memory, Task Queue, Communication)
- **🛠️ Builder Agent** (`agents/builder/`): AI Software Engineer (Code Generator, Tester, Documentation, Git Manager, Improvement Loop)
- **⚙️ DevOps Agent** (`agents/devops/`): Infrastructure Engineer (Docker Manager, Server Manager, Deployment, Monitoring, Backup)
- **📊 Trading Intelligence Agent** (`agents/trading/`): Financial Analysis Worker (Market Scanner, Strategy Engine, Risk Manager, Execution Bridge, Trade Journal)
- **🛡️ Guardian Agent** (`agents/guardian/`): Security & Safety (Access Control, Secret Manager, Threat Detection, Backup Check, Emergency Stop)
- **💻 Device Worker Agents** (`agents/workers/`): Mini PC Agent, Laptop Agent, USB Intelligence Agent

---

## 📁 Project Structure

```
GenX_FX/
├── agents/                 # GENX 3.6.9 Agent Mode System
│   ├── commander/          # Commander Agent
│   ├── builder/            # Builder Agent
│   ├── devops/             # DevOps Agent
│   ├── trading/            # Trading Intelligence Agent
│   ├── guardian/           # Guardian Agent
│   ├── workers/            # Mini PC, Laptop, USB Agents
│   └── common/             # MessageBus, Permissions, BaseAgent, Schemas
├── src/                    # Source code & main entrypoint
├── tests/                  # Test suite
├── data/                   # Memories, experiences, failures, improvements
├── scripts/                # Deployment scripts (deploy_jules.sh)
├── deploy.sh               # One-click deployment executable
├── DEPLOYMENT.md           # Deployment documentation
└── README.md               # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- VS Code or Cursor IDE

### Installation & Launch

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GenX_FX
   ```

2. Run One-Click Jules Deployment:
   ```bash
   ./deploy.sh
   ```

## 🧪 Testing
```bash
# Run all agent tests
python3 -m pytest
```

## 🔐 Security

- Secret sanitization and redaction via Guardian Secret Manager
- Access control verification with Permission Levels (LEVEL 0 to 5)
- Anomaly threat detection & emergency stop state machine

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
