# 🏗️ Architecture Index

GENX 3.6.9 Autonomous Device Intelligence Operating System Knowledge Graph.

```
Device Layer
      │
BLUEDIM Mini PC (Edge Local Brain)
      │
Docker Services & Container Runtimes
      │
FastAPI Bridge & Message Bus
      │
AI Agent Layer (Commander, Guardian, Builder, DevOps, Trading, Workers)
      │
Trading Engine & Risk Manager
      │
Broker / VPS / MT5 EA Bridge
```

## 🔄 System Communication & Data Flow

1. **Inter-Agent Communication**: Asynchronous pub/sub `MessageBus` (`agents/common/message_bus.py`).
2. **Permission Model**: Strict Level 0 (Read Only) to Level 5 (Financial Operations) checked by `PermissionManager` (`agents/common/permissions.py`).
3. **Secret Protection Flow**: AI Agent Action -> AI Secret Guardian Inspection -> Vault Policy Check -> Encrypted Vault -> Audit Logger.
4. **Network Ports**:
   - FastAPI Server: `8000`
   - Prometheus / Metrics: `9090` / `/metrics`
   - Redis: `6379`
