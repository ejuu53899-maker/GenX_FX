# Setup Scripts

This directory contains automation scripts for setting up and managing the Workspace Monorepo.

## Available Scripts

### Cross-Platform Scripts (Linux/Mac)

#### `full-setup.sh` ⭐ **Recommended**
Master setup script that runs the complete repository setup in one command.

```bash
bash scripts/full-setup.sh
```

**What it does:**
1. Runs basic repository setup (`setup.sh`)
2. Initializes all project directory structures (`init-all-projects.sh`)
3. Creates configuration file templates (`create-project-config.sh`)

---

#### `setup.sh`
Basic repository setup and verification.

```bash
bash scripts/setup.sh
```

**What it does:**
- ✅ Checks Git installation
- ✅ Verifies Bash version
- ✅ Configures Git user (if needed)
- ✅ Verifies remote configuration
- ✅ Validates repository structure

---

#### `init-all-projects.sh`
Creates directory structures for all projects.

```bash
bash scripts/init-all-projects.sh
```

**What it does:**
- Creates `src/`, `docs/`, `tests/` directories for each project
- Adds `.gitkeep` files to track empty directories

**Projects initialized:**
- MQL5-Google-Onedrive (src, include, docs, tests)
- OS-Twin (src, config, scripts, docs, tests)
- OS-Twin-setup (install, config, docs)
- AgentBrain (src, agents, config, docs, tests)

---

#### `create-project-config.sh`
Generates configuration templates for all projects.

```bash
bash scripts/create-project-config.sh
```

**What it does:**
- Creates `config.ini.example` files
- Creates `.env.example` files
- Configures project-specific settings

---

### Windows Scripts (PowerShell)

#### `setup.ps1`
Basic repository setup for Windows.

```powershell
.\scripts\setup.ps1
```

#### `init-all-projects.ps1`
Initialize project structures on Windows.

```powershell
.\scripts\init-all-projects.ps1
```

#### `create-project-config.ps1`
Create configuration templates on Windows.

```powershell
.\scripts\create-project-config.ps1
```

#### `configure-branch-protection.ps1`
Configure GitHub branch protection rules.

```powershell
.\scripts\configure-branch-protection.ps1
```

---

## Quick Start

### For Linux/Mac Users

```bash
# Clone the repository
git clone https://github.com/Mouy-leng/Workspace-Monorepo.git
cd Workspace-Monorepo

# Run full setup (recommended)
bash scripts/full-setup.sh
```

### For Windows Users

```powershell
# Clone the repository
git clone https://github.com/Mouy-leng/Workspace-Monorepo.git
cd Workspace-Monorepo

# Run setup
.\scripts\setup.ps1

# (Optional) Initialize project structures
.\scripts\init-all-projects.ps1

# (Optional) Create configuration templates
.\scripts\create-project-config.ps1
```

---

## After Setup

1. **Copy example configs to actual configs:**
   ```bash
   cp MQL5-Google-Onedrive/.env.example MQL5-Google-Onedrive/.env
   cp AgentBrain/.env.example AgentBrain/.env
   ```

2. **Edit configs with your credentials:**
   - Never commit actual `.env` or `config.ini` files
   - Only commit `.example` templates

3. **Start developing:**
   - Read [CONTRIBUTING.md](../CONTRIBUTING.md)
   - Review [DEVELOPMENT.md](../DEVELOPMENT.md)
   - Check project-specific README files

---

## Troubleshooting

### Permission Denied (Linux/Mac)

If you get permission denied errors, make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Execution Policy (Windows)

If PowerShell blocks script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Script Maintenance

- **Bash scripts** are for Linux/Mac/Unix environments
- **PowerShell scripts** are for Windows environments
- Both sets provide similar functionality
- Keep scripts synchronized when making changes
