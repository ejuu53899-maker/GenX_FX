#!/bin/bash
# Repository Setup Script
# Run this script to set up your development environment

set -e

echo "========================================"
echo "  WORKSPACE MONOREPO SETUP"
echo "========================================"
echo ""

# Check Git
echo "[1] Checking Git installation..."
if command -v git &> /dev/null; then
    git_version=$(git --version)
    echo "  ✅ $git_version"
else
    echo "  ❌ Git not found. Please install Git first."
    exit 1
fi

# Check Bash version
echo "[2] Checking Bash version..."
bash_version=$(bash --version | head -n 1)
echo "  ✅ $bash_version"

# Configure Git user (if not set)
echo "[3] Checking Git configuration..."
git_user=$(git config user.name || echo "")
git_email=$(git config user.email || echo "")

if [ -z "$git_user" ]; then
    echo "  ⚠️  Git user name not set"
    read -p "Enter your Git user name: " user_name
    git config user.name "$user_name"
    echo "  ✅ Git user name configured"
else
    echo "  ✅ Git user: $git_user"
fi

if [ -z "$git_email" ]; then
    echo "  ⚠️  Git email not set"
    read -p "Enter your Git email: " user_email
    git config user.email "$user_email"
    echo "  ✅ Git email configured"
else
    echo "  ✅ Git email: $git_email"
fi

# Verify remote
echo "[4] Checking Git remote..."
if remote=$(git remote get-url origin 2>&1); then
    echo "  ✅ Remote configured: $remote"
else
    echo "  ⚠️  Remote not configured"
    echo "  Run: git remote add origin https://github.com/Mouy-leng/Workspace-Monorepo.git"
fi

# Check repository structure
echo "[5] Verifying repository structure..."
required_dirs=("DomainController" "MQL5-Google-Onedrive" "OS-Twin" "OS-Twin-setup" "AgentBrain")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir exists"
    else
        echo "  ⚠️  $dir missing"
    fi
done

# Summary
echo ""
echo "========================================"
echo "  SETUP COMPLETE"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review CONTRIBUTING.md for contribution guidelines"
echo "  2. Read DEVELOPMENT.md for development workflow"
echo "  3. Start working on your project!"
echo ""
