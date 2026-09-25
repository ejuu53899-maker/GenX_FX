# 🔌 API Index

Index of REST APIs, Message Bus topics, WebSockets, and External Connectors.

## 📡 Inter-Agent Message Bus Topics

| Topic | Publisher | Subscribers | Purpose |
|---|---|---|---|
| `system.broadcast` | Guardian / Commander | All Agents | System-wide broadcasts & emergency stop commands |
| `agent.<agent_name>` | Any Agent | Target Agent | Direct point-to-point task assignment & response |
| `commander.register_agent` | Device Workers | Commander Agent | Agent node registration in Commander memory |
| `commander.task_response` | Any Agent | Commander Agent | Task execution status & payload results |
| `guardian.security_check` | Any Agent | Guardian Agent | Pre-execution threat and risk evaluation |
| `guardian.emergency_stop` | Any Agent | Guardian Agent | Manual emergency stop trigger request |

## 🌐 External Connectors

- **GitLab CI/CD API** (`connectors/gitlab.py`): Syncs environment variables to GitLab CI/CD variable store.
- **Firebase API** (`connectors/firebase.py`): Syncs Firestore database credentials and project authentication.
- **Google Cloud Secret Manager** (`connectors/google_cloud.py`): Cloud Secret Manager API connector.
- **MetaTrader5 EA Bridge** (`connectors/mt5.py`): Syncs MT5 broker credentials for automated trading.
