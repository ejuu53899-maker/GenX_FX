# GenX_FX Trading System

A comprehensive AI-powered foreign exchange trading system with advanced market analysis, automated trading capabilities, Google Cloud Data Agent Kit integration, Jules Always-On Trading Positioning System Engine, GENX LAN Secret/Variable Security Architecture, and GitHub Workspace 24/7 Live VS Code Server.

## 🚀 Key Features

- **🌐 GitHub Workspace 24/7 Live VS Code Server**:
  - **DevContainer Integration**: Pre-configured `.devcontainer/devcontainer.json` for GitHub Codespaces and VS Code Remote Containers with Python 3.11+, Node.js 18+, Docker-in-Docker, and auto-forwarded ports (8080 LAN, 8000 API, 5001 MT5).
  - **Continuous Keep-Alive Daemon**: `scripts/launch_vscode_247_server.sh` script to keep Jules engine and VS Code workspace running continuously 24/7.
  - **1-Click IDE Tasks**: Dedicated VS Code task `Launch GitHub Workspace 24/7 Live VS Code Server`.
- **🔐 GENX GitHub → LAN Secret & Network Architecture**:
  - **Variable/Secret Separation**: Strict isolation between non-secret variables (`GENX_LAN_HOST`, `GENX_LAN_PORT`, `GENX_API_PORT`, `GENX_DEVICE_NAME`, `GENX_ENVIRONMENT`, `GENX_CONTROL_MODE`) and encrypted secrets (`GENX_LAN_TOKEN`, `GENX_API_SECRET`, `GENX_SSH_PRIVATE_KEY`, `GENX_DEVICE_PASSWORD`, `GENX_WEBHOOK_SECRET`).
  - **Local Vault Isolation**: `vault/` directory for runtime keys with `.gitignore` enforcing non-commitment of secrets (`!.env.example`, `!vault/.gitkeep`, `!vault/README.md`).
  - **GitHub Actions Workflow**: Automated deployment (`.github/workflows/lan-deploy.yml`) fetching parameters securely via `${{ vars.* }}` and `${{ secrets.* }}` contexts.
  - **Secure Network Topology**: Encrypted `VPS -> VPN Tunnel -> Router -> Mini PC (LAN Controller :8080) -> MT5 / EA AI Bridge` path without exposing ports to the public internet.
- **Jules Always-On Trading Positioning System Engine**:
  - **1-Click Startup Launchers**: Executable `scripts/start_jules_always_on_engine.sh` (Linux/macOS) and `scripts/start_jules_always_on_engine.bat` (Windows)
  - **Mandatory Profit-Closing Rule**: Real-time ownership and profit-closing trade execution for all open symbols across markets
  - **Real-Time Symbol Manager**: Active tracking of floating profits, dynamic trailing stop locks, and guaranteed profit closes (`JulesPositionManager`)
- **Monorepo & Subproject Integration**:
  - Integrated `JetBrainsMono` and `ZOLO-A6-9VxNUNA-` repositories into `GenX_FX.code-workspace`
  - Version control sync and branch update manager (`scripts/sync_workspace.sh`)
- **Google Cloud Data Agent Kit**: Full starter pack and intelligent IDE interface for Google Cloud Data ecosystem
  - **BigQuery Connector & NL2SQL**: Natural language to BigQuery SQL translation and cost estimation
  - **Cloud Storage Data Lakes**: Automated ingestion and parquet dataset management
  - **Vertex AI Gemini Agent**: Autonomous data reasoning and market insight generation
  - **AI Data Agents**: Specialized agents for Analytics (`DataAnalystAgent`), Pipelines (`DataPipelineAgent`), Quality Audits (`DataQualityAgent`), and Security (`DataGovernanceAgent`)
  - **Starter Pack Scaffolding**: One-command project templates (`bigquery-analytics`, `financial-pipeline`, `realtime-stream`, `vertex-data-agent`)
  - **IDE Extensions & Tasks**: Preset workspace settings, tasks, and prompt context providers for Cursor IDE and VS Code

## 📁 Project Structure

```
GenX_FX/
├── .devcontainer/
│   └── devcontainer.json           # GitHub Codespaces & VS Code 24/7 Server devcontainer
├── .github/
│   └── workflows/
│       ├── lan-deploy.yml          # GitHub Actions LAN Controller deployment workflow
│       └── qodo-cover.yml          # Qodo Cover Agent workflow
├── .vscode/                        # VS Code tasks.json and settings.json
│   └── tasks.json
├── config/                         # Configuration files
│   ├── genx.yaml                   # System & vault settings
│   ├── lan.yaml                    # LAN controller & network topology parameters
│   └── ports.yaml                  # Port registry (LAN :8080, API :8000, MT5 :5001)
├── vault/                          # Secure local runtime key vault (git-ignored)
│   ├── README.md                   # Vault security isolation policy
│   └── .gitkeep
├── src/
│   ├── main.py                     # Main application entry point (--always-on mode)
│   ├── core/                       # Core engine modules
│   │   └── network/                # LAN Network Controller (`lan_controller.py`)
│   ├── trading/                    # Jules Real-Time Trading Position Manager Engine
│   │   └── jules_position_manager.py
│   └── cloud_data_agent_kit/       # Google Cloud Data Agent Kit
├── scripts/                        # Monorepo sync, LAN control, and 1-click launchers
│   ├── launch_vscode_247_server.sh # 24/7 GitHub Workspace & VS Code Server Keep-Alive
│   ├── lan_connect.sh              # LAN tunnel connection script
│   ├── lan_health.sh               # LAN target health check script
│   ├── lan_start.sh                # LAN controller start script
│   ├── lan_stop.sh                 # LAN controller stop script
│   ├── sync_workspace.sh           # Workspace monorepo subprojects sync script
│   ├── start_jules_always_on_engine.sh  # 1-Click Always-On Launcher (Linux/Mac)
│   └── start_jules_always_on_engine.bat # 1-Click Always-On Launcher (Windows)
├── JetBrainsMono/                  # Cloned JetBrainsMono monorepo subproject
├── ZOLO-A6-9VxNUNA-/               # Cloned ZOLO-A6-9VxNUNA- trading subproject
├── .env.example                    # Non-secret environment variable template
├── tests/                          # Unit and integration tests
├── requirements.txt                # Python dependencies
├── GenX_FX.code-workspace         # Multi-root VS Code workspace file
└── README.md                       # This file
```

## 🌐 24/7 GitHub Workspace & VS Code Server

To launch the 24/7 live VS Code workspace server:

```bash
# Launch 24/7 VS Code Server Keep-Alive script
./scripts/launch_vscode_247_server.sh
```

Or open in **GitHub Codespaces**:
1. Click **Code** -> **Codespaces** -> **Create codespace on main**.
2. DevContainer automatically installs dependencies and starts the 24/7 background service via `postStartCommand`.

## ⚡ 1-Click Jules Always-On Engine Launch

```bash
# Linux / macOS
./scripts/start_jules_always_on_engine.sh

# Windows Command Prompt / PowerShell
.\scripts\start_jules_always_on_engine.bat

# Python direct
python src/main.py --always-on
```

## 🛠️ LAN Control Scripts

```bash
# Health check target LAN device
./scripts/lan_health.sh

# Connect to LAN via secure VPN tunnel
./scripts/lan_connect.sh

# Start / Stop LAN Controller
./scripts/lan_start.sh
./scripts/lan_stop.sh
```

## 🔄 Monorepo Workspace Sync

```bash
./scripts/sync_workspace.sh
```

## 🧪 Testing
```bash
# Run all unit and integration tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
