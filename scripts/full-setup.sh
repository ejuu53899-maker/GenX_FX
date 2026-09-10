#!/bin/bash
# Full Setup Script - Runs all setup steps
# This script orchestrates the complete repository setup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "========================================"
echo "  WORKSPACE MONOREPO - FULL SETUP"
echo "========================================"
echo ""
echo "This script will:"
echo "  1. Run basic repository setup"
echo "  2. Initialize all project structures"
echo "  3. Create configuration templates"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

cd "$REPO_ROOT"

# Step 1: Basic setup
echo ""
echo "========================================"
echo "  STEP 1: Basic Repository Setup"
echo "========================================"
echo ""
bash "$SCRIPT_DIR/setup.sh"

# Step 2: Initialize projects
echo ""
echo "========================================"
echo "  STEP 2: Initialize Project Structures"
echo "========================================"
echo ""
bash "$SCRIPT_DIR/init-all-projects.sh"

# Step 3: Create configurations
echo ""
echo "========================================"
echo "  STEP 3: Create Configuration Files"
echo "========================================"
echo ""
bash "$SCRIPT_DIR/create-project-config.sh"

# Final summary
echo ""
echo "========================================"
echo "  🎉 FULL SETUP COMPLETE! 🎉"
echo "========================================"
echo ""
echo "Your workspace is now fully set up and ready!"
echo ""
echo "Quick verification:"
echo "  ✅ Git configured"
echo "  ✅ Project directories initialized"
echo "  ✅ Configuration templates created"
echo ""
echo "Next steps:"
echo "  1. Review the created directory structures"
echo "  2. Copy .example files to create your configs:"
echo "     cp MQL5-Google-Onedrive/.env.example MQL5-Google-Onedrive/.env"
echo "     cp AgentBrain/.env.example AgentBrain/.env"
echo "  3. Add your credentials to the .env files"
echo "  4. Read CONTRIBUTING.md and DEVELOPMENT.md"
echo "  5. Start coding!"
echo ""
echo "Documentation:"
echo "  📖 README.md - Overview and structure"
echo "  📖 QUICK_START.md - Quick start guide"
echo "  📖 CONTRIBUTING.md - Contribution guidelines"
echo "  📖 DEVELOPMENT.md - Development workflow"
echo ""
echo "Happy coding! 🚀"
echo ""
