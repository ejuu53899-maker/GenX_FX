# GENX Starter Kit v3.6.9 PowerShell Installer
# Owner: NUNA

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cy
Write-Host " GENX Starter Kit v3.6.9 Installer" -ForegroundColor Cy
Write-Host " Owner: NUNA" -ForegroundColor Cy
Write-Host "======================================" -ForegroundColor Cy

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "ERROR: Python is required."
    exit 1
}

Write-Host "[1/6] Creating virtual environment..."
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "[2/6] Upgrading packaging tools..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel --quiet

Write-Host "[3/6] Installing GENX dependencies..."
if (Test-Path "requirements.txt") {
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
}

Write-Host "[4/6] Creating runtime directories..."
$dirs = @("data\logs", "data\journal", "data\cache", "vault", "updates", "skills")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "[5/6] Running validation..."
& .\.venv\Scripts\python.exe -m pytest tests\ -q

Write-Host "`nGENX installation completed." -ForegroundColor Green
Write-Host "Activate: .\.venv\Scripts\Activate.ps1"
Write-Host "Start:    .\launcher\genx.ps1 start"
