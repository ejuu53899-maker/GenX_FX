# 💻 Code Intelligence Index

Index of primary source files, purpose, language, dependencies, and operational status.

| File Path | Language | Purpose | Dependencies | Status |
|---|---|---|---|---|
| `src/main.py` | Python 3.12 | Main application entrypoint, boots AgentOSOrchestrator | `agents.orchestrator`, `asyncio`, `logging` | Active |
| `agents/orchestrator.py` | Python 3.12 | 7-step startup sequence & emergency mode controller | `agents.common`, `agents.*` | Active |
| `agents/common/base_agent.py` | Python 3.12 | Base class for all GENX autonomous agents | `agents.common.schemas`, `message_bus` | Active |
| `agents/common/message_bus.py` | Python 3.12 | Async pub/sub inter-agent message routing bus | `agents.common.schemas`, `permissions` | Active |
| `agents/common/permissions.py` | Python 3.12 | Agent permission checking & authorization manager | `agents.common.schemas` | Active |
| `agents/common/learning_loop.py` | Python 3.12 | Experience logger, failure analyzer & skill evolver | `data/memories`, `data/experiences`, etc. | Active |
| `agents/commander/commander_agent.py` | Python 3.12 | Commander Agent (Central Brain) | `planner`, `decision_engine`, `memory` | Active |
| `agents/builder/builder_agent.py` | Python 3.12 | Builder Agent (AI Software Engineer) | `code_generator`, `tester`, `git_manager` | Active |
| `agents/devops/devops_agent.py` | Python 3.12 | DevOps Agent (Infrastructure Engineer) | `docker_manager`, `server_manager`, `backup` | Active |
| `agents/trading/trading_agent.py` | Python 3.12 | Trading Agent (Financial Analysis Worker) | `market_scanner`, `strategy_engine`, `risk_manager` | Active |
| `agents/guardian/guardian_agent.py` | Python 3.12 | Guardian Agent (Security & Safety) | `access_control`, `secret_manager`, `emergency_stop` | Active |
| `agents/workers/mini_pc.py` | Python 3.12 | Mini PC Device Worker (Local AI Server Node) | `agents.common.base_agent` | Active |
| `agents/workers/laptop.py` | Python 3.12 | Laptop Device Worker (Dev Command Center) | `agents.common.base_agent` | Active |
| `agents/workers/usb_intelligence.py` | Python 3.12 | USB Intelligence Worker (Portable Skill Installer) | `json`, `pathlib`, `schemas` | Active |
| `vault_core/vault_engine.py` | Python 3.12 | Master Vault Engine for secret encryption/storage | `encryption`, `key_manager`, `policy_engine` | Active |
| `vault_core/encryption.py` | Python 3.12 | AES-256 base64 symmetric encryption engine | `hashlib`, `base64` | Active |
| `security/ai_guardian.py` | Python 3.12 | AI Secret Guardian output scanner | `re`, `logging` | Active |
| `cli/genx_vault.py` | Python 3.12 | CLI tool for genx-vault operations | `argparse`, `vault_core`, `security` | Active |
| `deploy.sh` | Bash | One-click Jules deployment launcher | `scripts/deploy_jules.sh` | Active |
| `scripts/deploy_jules.sh` | Bash | Deployment setup, dependency check & launcher | `python3`, `pytest` | Active |
