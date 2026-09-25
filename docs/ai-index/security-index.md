# 🛡️ Security Knowledge Index

Security analysis, secret handling, AI guardian inspection, and permission policies.

## 🔐 Security Audit Summary

- **Secrets Handling**: Zero hardcoded secrets in source control. Credentials managed via `.env.vault/` and `vault_core/` encrypted files (`.enc`).
- **AI Secret Guardian** (`security/ai_guardian.py`): Scans agent code and prompt outputs to detect and block secret leaks (e.g. `print(private_key)`).
- **Agent Permission Levels**:
  - `LEVEL 0`: Read Only
  - `LEVEL 1`: Analyze
  - `LEVEL 2`: Create Files
  - `LEVEL 3`: Deploy
  - `LEVEL 4`: Execute Actions
  - `LEVEL 5`: Financial Operations
- **Sanitization & Redaction**: `SecretManager` sanitizes log outputs, replacing sensitive token values with `***REDACTED***`.
- **Emergency Stop Safeguard**: Guardian Agent triggers system freeze, stops live trading, freezes deployments, and notifies owner upon critical threat detection.
