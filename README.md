# GenX_FX Trading System & GENX Starter Kit v3.6.9

A comprehensive AI-powered foreign exchange trading system with advanced market analysis, automated trading capabilities, Google Cloud Data Agent Kit integration, Jules Always-On Trading Positioning System Engine, GENX LAN Secret/Variable Security Architecture, Exness MT5 EA Setup on Linux VPS, GENX Starter Kit v3.6.9 Installer & Extension Manager, and GitHub Workspace 24/7 Live VS Code Server.

## 🚀 Key Features

- **🎮 GENX Starter Kit v3.6.9 Installer & Unified Controller**:
  - **Clean Installation & Setup**: Dedicated installer script (`install/install_genx.sh` and `install/install_genx.ps1`) separating core setup from extension management.
  - **Unified Command Controller**: `./launcher/genx.sh` supporting `start`, `stop`, `restart`, `status`, `health`, `extensions`, `install-extension`, `update`, and `emergency-stop`.
  - **Extension & Skill Lifecycle Manager**: `./scripts/install_extension.sh` and Python extension manager (`scripts/genx_command.py`) with manifest validation, automated testing, isolated installation into `skills/`, and rollback.
- **📈 Exness MT5 EA Setup on Linux VPS**:
  - **Automated Linux VPS Installer**: Headless Wine, Xvfb, MetaTrader 5 Terminal, and Exness EA installer script (`scripts/install_exness_mt5_linux.sh`).
  - **Python Exness MT5 Bridge**: Socket/IPC connector for Exness MT5 account info and position fetching (`src/trading/exness_mt5_bridge.py`).
- **🌐 GitHub Workspace 24/7 Live VS Code Server**:
  - **DevContainer Integration**: Pre-configured `.devcontainer/devcontainer.json` for GitHub Codespaces and VS Code Remote Containers with Python 3.11+, Node.js 18+, Docker-in-Docker, and auto-forwarded ports (8080 LAN, 8000 API, 5001 MT5).
  - **Continuous Keep-Alive Daemon**: `scripts/launch_vscode_247_server.sh` script to keep Jules engine and VS Code workspace running continuously 24/7.
- **🔐 GENX GitHub → LAN Secret & Network Architecture**:
  - **Variable/Secret Separation**: Strict isolation between non-secret variables (`GENX_LAN_HOST`, `GENX_LAN_PORT`, `GENX_API_PORT`, `GENX_DEVICE_NAME`, `GENX_ENVIRONMENT`, `GENX_CONTROL_MODE`) and encrypted secrets (`GENX_LAN_TOKEN`, `GENX_API_SECRET`, `GENX_SSH_PRIVATE_KEY`, `GENX_DEVICE_PASSWORD`, `GENX_WEBHOOK_SECRET`).
  - **Local Vault Isolation**: `vault/` directory for runtime keys with `.gitignore` enforcing non-commitment of secrets (`!.env.example`, `!vault/.gitkeep`, `!vault/README.md`).
- **Jules Always-On Trading Positioning System Engine**:
  - **1-Click Startup Launchers**: Executable `scripts/start_jules_always_on_engine.sh` (Linux/macOS) and `scripts/start_jules_always_on_engine.bat` (Windows)
  - **Mandatory Profit-Closing Rule**: Real-time ownership and profit-closing trade execution for all open symbols across markets
- **Google Cloud Data Agent Kit**: Full starter pack and intelligent IDE interface for Google Cloud Data ecosystem

## 📁 Project Structure

```
GenX_FX/
├── install/                        # Core installer scripts
│   ├── install_genx.sh             # Linux/macOS installer
│   └── install_genx.ps1            # Windows PowerShell installer
├── launcher/                       # Unified command controller & lifecycle scripts
│   ├── genx.sh                     # Unified CLI launcher script
│   ├── genx.ps1                    # PowerShell launcher script
│   ├── start.sh                    # Core starter
│   ├── health_check.sh             # System health checker
│   ├── stop.sh                     # Process stopper
│   ├── update.sh                   # Workspace updater
│   └── emergency_stop.sh           # Emergency kill switch
├── scripts/                        # Extension installer & management utilities
│   ├── install_extension.sh        # Extension/skill installer (Linux/Mac)
│   ├── install_extension.ps1       # Extension/skill installer (Windows)
│   ├── genx_command.py             # Extension lifecycle manager
│   ├── install_exness_mt5_linux.sh # Exness MT5 EA Linux VPS installer
│   ├── launch_monitoring.sh        # System monitoring launcher script
│   ├── launch_vscode_247_server.sh # 24/7 GitHub Workspace & VS Code Server Keep-Alive
│   └── sync_workspace.sh           # Workspace monorepo subprojects sync script
├── .devcontainer/
│   └── devcontainer.json           # GitHub Codespaces & VS Code 24/7 Server devcontainer
├── .github/
│   └── workflows/
│       ├── lan-deploy.yml          # GitHub Actions LAN Controller deployment workflow
│       └── qodo-cover.yml          # Qodo Cover Agent workflow
├── .vscode/                        # VS Code tasks.json and settings.json
├── config/                         # Configuration files (genx.yaml, lan.yaml, ports.yaml)
├── vault/                          # Secure local runtime key vault (git-ignored)
├── src/
│   ├── main.py                     # Main application entry point (--always-on mode)
│   ├── core/                       # Core engine modules (`lan_controller.py`)
│   ├── trading/                    # Jules Real-Time Position Manager & Exness MT5 Bridge
│   └── cloud_data_agent_kit/       # Google Cloud Data Agent Kit
├── tests/                          # Unit and integration tests
├── requirements.txt                # Python dependencies
├── GenX_FX.code-workspace         # Multi-root VS Code workspace file
└── README.md                       # This file
```

## 🛠️ GENX Starter Kit Installation & Commands

### Installation
```bash
# Install GENX Starter Kit
chmod +x install/install_genx.sh
./install/install_genx.sh
```

### Unified Launcher Commands
```bash
./launcher/genx.sh start
./launcher/genx.sh health
./launcher/genx.sh status
./launcher/genx.sh extensions
./launcher/genx.sh install-extension ./my-extension-path
./launcher/genx.sh update
./launcher/genx.sh emergency-stop
```

### Installing Extensions/Skills
```bash
./scripts/install_extension.sh ./my-extension-directory
```

## 📈 Exness MT5 EA Setup on Linux VPS

```bash
./scripts/install_exness_mt5_linux.sh
```

## 🌐 24/7 GitHub Workspace & VS Code Server

```bash
./scripts/launch_vscode_247_server.sh
```

## 🧪 Testing
```bash
# Run all unit and integration tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
