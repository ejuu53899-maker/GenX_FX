#!/bin/bash
# Initialize All Empty Projects
# Creates basic structure for all project directories

set -e

echo "========================================"
echo "  INITIALIZING PROJECT STRUCTURES"
echo "========================================"
echo ""

# Function to create directory structure
initialize_project() {
    local project_path=$1
    shift
    local sub_directories=("$@")

    echo "Initializing: $project_path"

    if [ ! -d "$project_path" ]; then
        mkdir -p "$project_path"
    fi

    for dir in "${sub_directories[@]}"; do
        local full_path="$project_path/$dir"
        if [ ! -d "$full_path" ]; then
            mkdir -p "$full_path"
            echo "  ✅ Created: $dir"
        else
            echo "  ⚠️  Exists: $dir"
        fi
    done
}

# Initialize MQL5-Google-Onedrive
echo "[1] MQL5-Google-Onedrive"
initialize_project "MQL5-Google-Onedrive" "src" "include" "docs" "tests"

# Initialize OS-Twin
echo "[2] OS-Twin"
initialize_project "OS-Twin" "src" "config" "scripts" "docs" "tests"

# Initialize OS-Twin-setup
echo "[3] OS-Twin-setup"
initialize_project "OS-Twin-setup" "install" "config" "docs"

# Initialize AgentBrain
echo "[4] AgentBrain"
initialize_project "AgentBrain" "src" "agents" "config" "docs" "tests"

echo ""
echo "========================================"
echo "  INITIALIZATION COMPLETE"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review project structures"
echo "  2. Add project-specific files"
echo "  3. Update README files with project details"
echo "  4. Commit changes: git add . && git commit -m 'chore: Initialize project structures'"
echo ""
