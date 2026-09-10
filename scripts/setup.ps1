# Repository Setup Script
# Run this script to set up your development environment

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  WORKSPACE MONOREPO SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Git
Write-Host "[1] Checking Git installation..." -ForegroundColor Cyan
try {
    $gitVersion = git --version
    Write-Host "  ✅ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check PowerShell version
Write-Host "[2] Checking PowerShell version..." -ForegroundColor Cyan
$psVersion = $PSVersionTable.PSVersion
Write-Host "  ✅ PowerShell $psVersion" -ForegroundColor Green

# Configure Git user (if not set)
Write-Host "[3] Checking Git configuration..." -ForegroundColor Cyan
$gitUser = git config user.name
$gitEmail = git config user.email

if (-not $gitUser) {
    Write-Host "  ⚠️  Git user name not set" -ForegroundColor Yellow
    $userName = Read-Host "Enter your Git user name"
    git config user.name $userName
    Write-Host "  ✅ Git user name configured" -ForegroundColor Green
} else {
    Write-Host "  ✅ Git user: $gitUser" -ForegroundColor Green
}

if (-not $gitEmail) {
    Write-Host "  ⚠️  Git email not set" -ForegroundColor Yellow
    $userEmail = Read-Host "Enter your Git email"
    git config user.email $userEmail
    Write-Host "  ✅ Git email configured" -ForegroundColor Green
} else {
    Write-Host "  ✅ Git email: $gitEmail" -ForegroundColor Green
}

# Verify remote
Write-Host "[4] Checking Git remote..." -ForegroundColor Cyan
$remote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Remote configured: $remote" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Remote not configured" -ForegroundColor Yellow
    Write-Host "  Run: git remote add origin https://github.com/Mouy-leng/Workspace-Monorepo.git" -ForegroundColor Gray
}

# Check repository structure
Write-Host "[5] Verifying repository structure..." -ForegroundColor Cyan
$requiredDirs = @("DomainController", "MQL5-Google-Onedrive", "OS-Twin", "OS-Twin-setup", "AgentBrain")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✅ $dir exists" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $dir missing" -ForegroundColor Yellow
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review CONTRIBUTING.md for contribution guidelines" -ForegroundColor White
Write-Host "  2. Read DEVELOPMENT.md for development workflow" -ForegroundColor White
Write-Host "  3. Start working on your project!" -ForegroundColor White
Write-Host ""
