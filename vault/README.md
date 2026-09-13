# GENX Secure Local Vault Directory

🔐 **SECURITY NOTICE**:
This directory is reserved for local, runtime-only encrypted credentials and secret key storage.

## Security Policies
- **NEVER COMMIT REAL SECRETS TO GIT**: `.gitignore` is configured to ignore all files under `vault/*` except `README.md` and `.gitkeep`.
- Secrets are dynamically injected into the GENX application from **GitHub Actions Secrets** or local encrypted vault engines.
- Secrets stored locally must be encrypted at rest using AES-256.
