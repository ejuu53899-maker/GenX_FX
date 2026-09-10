#!/bin/bash
# Create Project Configuration Files
# Generates basic configuration files for each project

set -e

echo "========================================"
echo "  CREATING PROJECT CONFIGURATIONS"
echo "========================================"
echo ""

# MQL5-Google-Onedrive config
echo "[1] Creating MQL5-Google-Onedrive config..."
cat > "MQL5-Google-Onedrive/config.ini.example" << 'EOF'
# MQL5-Google-Onedrive Configuration

[GoogleDrive]
# Google OAuth Client ID
ClientID=YOUR_CLIENT_ID
ClientSecret=YOUR_CLIENT_SECRET

# Sync Settings
SyncInterval=300
AutoSync=true
SyncDirection=bidirectional

# File Filters
IncludePatterns=*.mq5,*.mqh,*.ex5
ExcludePatterns=*.log,*.tst
MaxFileSize=10485760

# Backup Settings
AutoBackup=true
BackupInterval=3600
KeepBackups=10
EOF
echo "  ✅ Created config.ini.example"

# OS-Twin config
echo "[2] Creating OS-Twin config..."
cat > "OS-Twin/config.ini.example" << 'EOF'
# OS-Twin Configuration

[Storage]
BackupLocation=/var/lib/os-twin/backups
CompressionLevel=6
MaxStorageSize=107374182400

[Sync]
SyncInterval=3600
ConflictResolution=ask
AutoSync=false

[General]
MaxSnapshots=10
SnapshotRetentionDays=30
EOF
echo "  ✅ Created config.ini.example"

# AgentBrain config
echo "[3] Creating AgentBrain config..."
cat > "AgentBrain/config.ini.example" << 'EOF'
# AgentBrain Configuration

[AI]
ModelProvider=openai
ModelName=gpt-4
Temperature=0.7
MaxTokens=2000

[Memory]
VectorDatabase=chroma
MemoryLimit=1000
ContextWindow=4096

[Tasks]
MaxConcurrentTasks=5
TaskTimeout=300
RetryAttempts=3

[API]
Port=8000
Host=localhost
EnableAuth=true
EOF
echo "  ✅ Created config.ini.example"

# Create .env.example files
echo "[4] Creating .env.example files..."

cat > "MQL5-Google-Onedrive/.env.example" << 'EOF'
# Google Drive API Credentials
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8080/callback

# MQL5 Settings
MQL5_DATA_PATH=/path/to/metatrader/data
EOF

cat > "AgentBrain/.env.example" << 'EOF'
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4
TEMPERATURE=0.7

# Database Configuration
DATABASE_URL=sqlite:///agentbrain.db
VECTOR_DB_PATH=./data/vector_db

# API Configuration
API_PORT=8000
API_HOST=localhost
SECRET_KEY=your_secret_key_here
EOF
echo "  ✅ Created .env.example files"

echo ""
echo "========================================"
echo "  CONFIGURATION FILES CREATED"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review configuration files"
echo "  2. Copy .example files and customize"
echo "  3. Add actual credentials (never commit!)"
echo "  4. Commit configuration templates"
echo ""
