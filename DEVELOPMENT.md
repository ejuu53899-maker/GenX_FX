# Development Guide

## Quick Start

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mouy-leng/Workspace-Monorepo.git
   cd Workspace-Monorepo
   ```

2. **Run full setup**

   For **Linux/Mac**:
   ```bash
   bash scripts/full-setup.sh
   ```

   For **Windows** (PowerShell):
   ```powershell
   .\scripts\setup.ps1
   ```

3. **Verify setup**
   ```bash
   git status
   git remote -v
   ```

## Development Environment

### Required Tools

- **Git** - Version control
- **Bash 4.0+** or **PowerShell 5.1+** - For automation scripts
- **Python 3.11+** - For Python projects (if applicable)
- **VS Code** (recommended) - Code editor

### VS Code Setup

Recommended extensions:
- PowerShell
- Python
- GitLens
- Markdown All in One

## Project Structure

```
Workspace-Monorepo/
├── DomainController/      # Domain controller scripts
├── MQL5-Google-Onedrive/  # MQL5 integration
├── OS-Twin/              # OS-Twin project
├── OS-Twin-setup/        # Setup scripts
├── AgentBrain/           # AgentBrain project
├── .github/              # GitHub workflows and templates
├── README.md             # Main documentation
└── CONTRIBUTING.md       # Contribution guidelines
```

## Common Tasks

### Adding a New Feature

1. Create feature branch:
   ```bash
   git checkout -b feature/feature-name
   ```

2. Make changes in appropriate directory

3. Test your changes

4. Commit:
   ```bash
   git add .
   git commit -m "feat(Project): Add feature description"
   ```

5. Push and create PR:
   ```bash
   git push origin feature/feature-name
   ```

### Updating Documentation

Documentation files:
- `README.md` - Main repository documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `DEVELOPMENT.md` - This file
- Project-specific docs in each subdirectory

### Running Scripts

**DomainController scripts:**
```powershell
cd DomainController
.\script-name.ps1
```

## Git Workflow

### Branch Naming

- `main` - Production branch
- `develop` - Development branch
- `feature/name` - New features
- `fix/name` - Bug fixes
- `docs/name` - Documentation updates

### Commit Messages

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Tests
- `chore:` - Maintenance

## CI/CD

GitHub Actions workflows:
- **CI** - Runs on push/PR
  - Lint checks
  - Structure validation
  - Build verification

## Troubleshooting

### Git Issues

**Problem**: Remote repository not found
```bash
git remote set-url origin https://github.com/Mouy-leng/Workspace-Monorepo.git
```

**Problem**: Authentication issues
```bash
git config credential.helper store
```

### PowerShell Issues

**Problem**: Execution policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [PowerShell Documentation](https://docs.microsoft.com/powershell)
- [GitHub Actions](https://docs.github.com/actions)

## Getting Help

1. Check existing documentation
2. Review GitHub issues
3. Create a new issue for questions
