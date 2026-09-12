# GenX_FX Trading System

A comprehensive AI-powered foreign exchange trading system with advanced market analysis, automated trading capabilities, Google Cloud Data Agent Kit integration, and Jules Always-On Trading Positioning System Engine.

## 🚀 Key Features

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
- **AI-Powered Analysis**: Advanced machine learning models for market prediction
- **Automated Trading**: Intelligent trading algorithms with risk management

## 📁 Project Structure

```
GenX_FX/
├── src/
│   ├── main.py                     # Main application entry point (--always-on mode)
│   ├── trading/                    # Jules Real-Time Trading Position Manager Engine
│   │   └── jules_position_manager.py
│   └── cloud_data_agent_kit/       # Google Cloud Data Agent Kit
│       ├── agents/                 # Analyst, Pipeline, Quality, Governance AI Agents
│       ├── connectors/             # BigQuery, GCS, Vertex AI connectors
│       ├── starter_pack/           # Templates and scaffolding generator
│       ├── ide_integration/        # VS Code / Cursor IDE providers & prompt context
│       └── cli.py                  # `cloud-data-agent` CLI interface
├── scripts/                        # Monorepo sync and 1-click engine launcher scripts
│   ├── sync_workspace.sh           # Workspace monorepo subprojects sync script
│   ├── start_jules_always_on_engine.sh  # 1-Click Always-On Launcher (Linux/Mac)
│   └── start_jules_always_on_engine.bat # 1-Click Always-On Launcher (Windows)
├── JetBrainsMono/                  # Cloned JetBrainsMono monorepo subproject
├── ZOLO-A6-9VxNUNA-/               # Cloned ZOLO-A6-9VxNUNA- trading subproject
├── tests/                          # Unit and integration tests
├── docs/                           # Documentation
├── config/                         # Configuration files
├── .vscode/                        # VS Code workspace settings and tasks
├── .cursor/                        # Cursor IDE settings and AI rules
├── requirements.txt                # Python dependencies
├── GenX_FX.code-workspace         # Multi-root VS Code workspace file
└── README.md                       # This file
```

## ⚡ 1-Click Jules Always-On Engine Launch

Launch the Jules Always-On Trading Positioning System Engine with a single click or command:

```bash
# Linux / macOS
./scripts/start_jules_always_on_engine.sh

# Windows Command Prompt / PowerShell
.\scripts\start_jules_always_on_engine.bat

# Python direct
python src/main.py --always-on
```

### Real-Time Symbol Profit-Closing Rule
Under Jules management, all open symbols are continuously monitored in the real-time market:
1. Floating profits are recalculated on every tick.
2. Dynamic trailing profit locks trigger as profits increase.
3. Every trade is closed with guaranteed positive realized profit.

## 🔄 Monorepo Workspace Sync

To sync and merge all workspace subprojects (`JetBrainsMono` and `ZOLO-A6-9VxNUNA-`):

```bash
./scripts/sync_workspace.sh
```

## ☁️ Cloud Data Agent Kit

### CLI Commands
```bash
# List available starter packs
python -m cloud_data_agent_kit.cli list-starters

# Scaffold a new BigQuery analytics starter pack project
python -m cloud_data_agent_kit.cli scaffold --template bigquery-analytics --dir ./my_data_starter

# Run natural language query via Data Analyst Agent
python -m cloud_data_agent_kit.cli query --prompt "Show top market pairs by volume"

# Run automated data quality audit on BigQuery table
python -m cloud_data_agent_kit.cli audit --dataset market_data --table ticks
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- VS Code or Cursor IDE

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GenX_FX
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python src/main.py --always-on
   ```

## 🧪 Testing
```bash
# Run all tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
