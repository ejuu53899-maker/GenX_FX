# Quick Start Guide

Get started with the Workspace Monorepo in 5 minutes!

## ✅ Prerequisites Check

Run this to verify your environment:
```powershell
# Check Git
git --version

# Check PowerShell
$PSVersionTable.PSVersion

# Check Python (if needed)
python --version
```

## 🚀 Quick Start Steps

### Step 1: Verify Repository Status
```powershell
cd F:\Workspace\Workspace-Monorepo
git status
git branch
```

**Expected Output:**
- Current branch: `develop`
- Working tree: clean
- Branches: `main`, `develop`

### Step 2: Run Setup Script

**For Linux/Mac:**
```bash
bash scripts/full-setup.sh
```

**For Windows (PowerShell):**
```powershell
.\scripts\setup.ps1
```

This will:
- ✅ Check Git installation
- ✅ Verify shell version (Bash/PowerShell)
- ✅ Configure Git user (if needed)
- ✅ Verify remote configuration
- ✅ Check repository structure
- ✅ Initialize all project directories
- ✅ Create configuration templates

### Step 3: Choose a Project

**Available Projects:**
1. **DomainController** - Active (21 files)
2. **MQL5-Google-Onedrive** - Ready for development
3. **OS-Twin** - Ready for development
4. **AgentBrain** - Ready for development
5. **OS-Twin-setup** - Ready for development

### Step 4: Create Your First Feature Branch

```powershell
# Example: Working on MQL5-Google-Onedrive
git checkout -b feature/mql5/add-sync-feature

# Or for DomainController
git checkout -b feature/domaincontroller/enhance-backup
```

### Step 5: Start Development

```powershell
# Navigate to your project
cd MQL5-Google-Onedrive  # or your chosen project

# Review requirements
cat requirements.md

# Set up configuration (if needed)
copy config.ini.example config.ini
copy .env.example .env
# Edit config.ini and .env with your values
```

### Step 6: Make Your First Commit

```powershell
# Make changes to files
# Stage changes
git add .

# Commit with conventional commit format
git commit -m "feat(mql5): Add initial sync functionality"

# Push to remote
git push origin feature/mql5/add-sync-feature
```

### Step 7: Create Pull Request

1. Go to: https://github.com/Mouy-leng/Workspace-Monorepo
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out PR template
5. Submit for review

## 📋 Quick Commands Reference

### Git Commands
```powershell
# Check status
git status

# View branches
git branch -a

# Create feature branch
git checkout -b feature/[project]/[feature-name]

# Commit changes
git add .
git commit -m "type(project): Description"

# Push changes
git push origin feature/[project]/[feature-name]

# Pull latest changes
git pull origin develop
```

### Project Commands
```powershell
# Initialize all projects
.\scripts\init-all-projects.ps1

# Create project configs
.\scripts\create-project-config.ps1

# Setup repository
.\scripts\setup.ps1
```

## 🎯 Common Workflows

### Starting a New Feature
```powershell
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/[project]/[feature-name]

# 3. Make changes and commit
git add .
git commit -m "feat([project]): Description"

# 4. Push and create PR
git push origin feature/[project]/[feature-name]
```

### Updating Your Branch
```powershell
# 1. Switch to develop
git checkout develop
git pull origin develop

# 2. Update your feature branch
git checkout feature/[project]/[feature-name]
git merge develop

# 3. Resolve conflicts if any
# 4. Push updates
git push origin feature/[project]/[feature-name]
```

## 📚 Documentation Quick Links

- [README.md](README.md) - Main documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow
- [ROADMAP.md](ROADMAP.md) - Project roadmap
- [NEXT_PHASE.md](NEXT_PHASE.md) - Development readiness

## 🔍 Verify Everything Works

Run this checklist:
```powershell
# ✅ Git configured
git config user.name
git config user.email

# ✅ Remote configured
git remote -v

# ✅ Branches exist
git branch -a

# ✅ Projects initialized
dir MQL5-Google-Onedrive
dir OS-Twin
dir AgentBrain

# ✅ CI/CD active
# Check: https://github.com/Mouy-leng/Workspace-Monorepo/actions
```

## 🆘 Troubleshooting

### Git Issues
```powershell
# Reset to clean state
git reset --hard HEAD

# Remove untracked files
git clean -fd

# Fix line endings
git config core.autocrlf true
```

### Authentication Issues
```powershell
# Re-authenticate
git config credential.helper store
```

### Branch Issues
```powershell
# Delete local branch
git branch -d feature/[branch-name]

# Delete remote branch
git push origin --delete feature/[branch-name]
```

## ✨ Next Steps

1. ✅ Repository setup complete
2. ✅ Projects initialized
3. ✅ Documentation ready
4. 🎯 **Start coding!**

Choose a project and begin development. Happy coding! 🚀

---

**Need Help?**
- Check [CONTRIBUTING.md](CONTRIBUTING.md)
- Review [DEVELOPMENT.md](DEVELOPMENT.md)
- Create an issue on GitHub
