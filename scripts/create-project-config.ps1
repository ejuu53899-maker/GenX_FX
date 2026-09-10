# PowerShell script to create configuration files for all projects
# Can be run independently or imported by setup.ps1

param (
    [string]$monorepoPath = (Split-Path -Parent $PSScriptRoot)
)

Write-Host "Creating configuration files for all projects..." -ForegroundColor Cyan
Write-Host "Monorepo path: $monorepoPath" -ForegroundColor Gray

# Define projects and their configs
$projects = @(
    @{
        Name = "AgentBrain"
        ConfigFile = "config.ini"
        ExampleFile = "config.ini.example"
    },
    @{
        Name = "OS-Twin"
        ConfigFile = "config.ini"
        ExampleFile = "config.ini.example"
    },
    @{
        Name = "MQL5-Google-Onedrive"
        ConfigFile = "config.ini"
        ExampleFile = "config.ini.example"
    }
)

foreach ($project in $projects) {
    $projectDir = Join-Path $monorepoPath $project.Name
    $configPath = Join-Path $projectDir $project.ConfigFile
    $examplePath = Join-Path $projectDir $project.ExampleFile

    if (Test-Path $projectDir) {
        if (-not (Test-Path $configPath)) {
            if (Test-Path $examplePath) {
                Copy-Item $examplePath $configPath
                Write-Host "  [+] Created $($project.ConfigFile) for $($project.Name)" -ForegroundColor Green
            } else {
                Write-Host "  [-] Example file not found for $($project.Name)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  [*] Config file already exists for $($project.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [-] Project directory not found: $($project.Name)" -ForegroundColor Red
    }
}

Write-Host "`nConfiguration creation complete!" -ForegroundColor Cyan
