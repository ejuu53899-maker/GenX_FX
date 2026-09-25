# 🌲 Environment Index

Folder-based environment vault template structure in `.env.vault/` and `templates/`.

## 📁 Environment Vault Layout

```
.env.vault/
├── development/        # Local development environment configs
├── staging/            # Staging & testing environment configs
├── production/         # Production deployment configs
├── backup/             # Vault backup snapshots
├── rotation/           # Key rotation logs
├── rules/              # Security policy markdown rules
├── logs/               # Audit logs
└── metadata/           # Vault metadata
```

## 📄 Service Environment Templates (`templates/`)

- `templates/gitlab.env.template`
- `templates/firebase.env.template`
- `templates/google.env.template`
- `templates/gemini.env.template`
- `templates/mt5.env.template`
- `templates/telegram.env.template`
- `templates/docker.env.template`
