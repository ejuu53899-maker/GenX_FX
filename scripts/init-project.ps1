# Initialize a New Project Directory
# Sets up a new project directory with basic structure

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [Parameter(Mandatory=$false)]
    [string]$ProjectType = "general"
)

$ErrorActionPreference = "Continue"

Write-Host "Initializing project: $ProjectName" -ForegroundColor Cyan

$projectPath = Join-Path $PSScriptRoot ".." $ProjectName

if (Test-Path $projectPath) {
    Write-Host "⚠️  Directory already exists: $projectPath" -ForegroundColor Yellow
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 0
    }
} else {
    New-Item -ItemType Directory -Path $projectPath -Force | Out-Null
}

# Create basic structure
$readmePath = Join-Path $projectPath "README.md"
$readmeContent = @"
# $ProjectName

Project description goes here.

## Setup

Setup instructions here.

## Usage

Usage instructions here.

## Contributing

See main repository CONTRIBUTING.md for guidelines.
"@

Set-Content -Path $readmePath -Value $readmeContent

# Create .gitkeep if directory is empty
$gitkeepPath = Join-Path $projectPath ".gitkeep"
if (-not (Test-Path $gitkeepPath)) {
    New-Item -ItemType File -Path $gitkeepPath -Force | Out-Null
}

Write-Host "✅ Project initialized: $projectPath" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Add project files to $projectPath" -ForegroundColor White
Write-Host "  2. Update README.md with project details" -ForegroundColor White
Write-Host "  3. Commit and push your changes" -ForegroundColor White
