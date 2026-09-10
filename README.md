# GenX_FX & Workspace Monorepo Integrated System

A comprehensive AI-powered foreign exchange trading system and multi-agent workspace monorepo integration with advanced market analysis, automated trading capabilities, and OS-Twin / AgentBrain orchestration.

## 🚀 Overview & Features

- **AI-Powered Analysis & AgentBrain**: Advanced machine learning models for market prediction and agent OS coordination.
- **Real-time Data & MQL5 Synchronization**: Live market data integration from multiple sources including MT5, Google Drive, and OneDrive sync.
- **Automated Trading & Domain Control**: Intelligent trading algorithms with risk management and domain controller automation scripts.
- **OS-Twin & Setup**: System twin replication and automated deployment tools.
- **Jules CLI & Tools Integration**: Command line control for continuous workspace syncing, agent plugins, and repository management.

## 📁 Integrated Workspace Structure

```
Workspace / GenX_FX Monorepo
├── src/                      # GenX_FX Core source code
├── AgentBrain/               # AI Agent Brain modules and configuration
├── DomainController/         # Domain control scripts and drive management
├── MQL5-Google-Onedrive/     # MQL5 cloud & drive sync integration
├── OS-Twin/                  # OS Twin framework
├── OS-Twin-setup/            # OS Twin setup utilities
├── scripts/                  # Project initialization and sync scripts
├── cli/                      # Jules CLI and agent utilities
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
├── config/                   # Configuration files
├── .vscode/                  # VS Code configuration
├── requirements.txt          # Python dependencies
├── GenX_FX.code-workspace   # Multi-folder workspace configuration
└── README.md                 # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- VS Code, Cursor IDE, or JetBrains IntelliJ IDEA

### Installation & Initialization

1. Clone or open the workspace:
   ```bash
   cd /app
   ```

2. Initialize subprojects using the provided scripts:
   ```bash
   ./scripts/setup.sh
   ./scripts/init-all-projects.sh
   ```

3. Run Jules CLI for workspace status and continuous syncing:
   ```bash
   jules status
   jules sync --start
   ```

## 💻 JetBrains & VS Code Integration

- **JetBrains IDE**: Deep Git4Idea integration (`jetbrains://idea/checkout/git?idea.required.plugins.id=Git4Idea&checkout.repo=git%40gitlab.com%3Agenxfx%2Fvscode-powershell.git`)
- **VS Code / Cursor Workspace**: Open `GenX_FX.code-workspace` to access all integrated sub-projects and recommended extensions (`ms-vscode.powershell`, `Git4Idea`).

## 🧪 Testing
```bash
python3 src/main.py
```

## 📝 License & Disclaimer

Educational and research software. Trading involves risk.
