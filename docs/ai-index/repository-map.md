# 🗺️ Repository Map

Complete directory and component mapping for GENX 3.6.9 Agent OS.

## 📂 Core Directories

```
GenX_FX/
├── agents/                 # GENX 3.6.9 AI Agent Ecosystem
│   ├── commander/          # Commander Agent (Central Brain, Planner, Decision Engine, Memory)
│   ├── builder/            # Builder Agent (Software Engineer, Code Gen, Tester, Git)
│   ├── devops/             # DevOps Agent (Infrastructure, Docker, Monitoring, Backup)
│   ├── trading/            # Trading Agent (Market Scanner, Strategy Engine, Risk Manager, Execution)
│   ├── guardian/           # Guardian Agent (Access Control, Secret Manager, Threat Detection, Emergency Stop)
│   ├── workers/            # Device Workers (Mini PC, Laptop, USB Intelligence)
│   └── common/             # BaseAgent, MessageBus, Permissions, LearningLoop, Schemas
├── vault_core/             # GENX Secret Vault Core Engine
│   ├── vault_engine.py     # Master Vault Engine
│   ├── encryption.py       # AES-256 Symmetric Encryption Engine
│   ├── key_manager.py      # Hardware/Master Key Manager
│   ├── policy_engine.py    # Agent Secret Access Policy Engine
│   └── audit_logger.py     # Audit Logger
├── security/               # Security Policies & AI Guardian
│   ├── ai_guardian.py      # AI Secret Exposure Scanner & Guardian
│   └── *.yaml              # Secret patterns, rotation, and access policies
├── cli/                    # Command Line Interfaces
│   └── genx_vault.py       # genx-vault CLI tool
├── connectors/             # Service Secret Connectors (GitLab, Firebase, GCP, MT5)
├── templates/              # Environment Vault Templates
├── monitoring/             # Vault Heartbeat & Security Alerts
├── src/                    # System Entrypoint (`src/main.py`)
├── tests/                  # Pytest Unit & Integration Test Suite
├── docs/                   # Documentation & AI Knowledge Index (`docs/ai-index/`)
├── data/                   # Memories, Experiences, Failures, Improvements
├── scripts/                # Deployment Scripts (`deploy_jules.sh`)
├── deploy.sh               # One-click deployment executable
└── README.md               # Main Ecosystem README
```

## 🔗 Component Relationships

- `src/main.py` -> initializes `AgentOSOrchestrator` (`agents/orchestrator.py`)
- `agents/orchestrator.py` -> coordinates `Guardian`, `Commander`, `Builder`, `DevOps`, `Trading`, and `Workers` via `MessageBus`
- `GuardianAgent` -> uses `SecretManager` (`agents/guardian/secret_manager.py`) which delegates to `VaultEngine` (`vault_core/`) and `AISecretGuardian` (`security/`)
- `cli/genx_vault.py` -> interfaces directly with `VaultEngine` and `AISecretGuardian` for security management
