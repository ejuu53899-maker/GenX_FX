# PowerShell script to initialize all projects in the monorepo
# Run this script to set up virtual environments and dependencies for all sub-projects

param (
    [string]$monorepoPath = (Split-Path -Parent $PSScriptRoot)
)

Write-Host "Initializing all monorepo projects..." -ForegroundColor Cyan
Write-Host "Monorepo path: $monorepoPath" -ForegroundColor Gray

# Sub-projects list
$projects = @("AgentBrain", "OS-Twin", "MQL5-Google-Onedrive")

foreach ($project in $projects) {
    $projectDir = Join-Path $monorepoPath $project
    Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
    Write-Host "Processing $project..." -ForegroundColor Yellow

    if (Test-Path $projectDir) {
        Push-Location $projectDir

        # Create virtual environment if it doesn't exist
        $venvDir = Join-Path $projectDir "venv"
        if (-not (Test-Path $venvDir)) {
            Write-Host "  Creating virtual environment..." -ForegroundColor Gray
            python -m venv venv
        } else {
            Write-Host "  Virtual environment already exists." -ForegroundColor Gray
        }

        # Install requirements if file exists
        $reqFile = Join-Path $projectDir "requirements.txt"
        if (Test-Path $reqFile) {
            Write-Host "  Installing dependencies..." -ForegroundColor Gray
            & "$venvDir\Scripts\pip.exe" install -r $reqFile
        } else {
            Write-Host "  No requirements.txt found." -ForegroundColor Gray
        }

        Pop-Location
    } else {
        Write-Host "  Directory not found: $projectDir" -ForegroundColor Red
    }
}

Write-Host "`nAll projects initialized!" -ForegroundColor Green
