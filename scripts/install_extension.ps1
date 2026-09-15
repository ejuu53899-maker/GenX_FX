# GENX Extension Installer PowerShell Script v3.6.9

param (
    [Parameter(Mandatory=$true)]
    [string]$ExtensionPath
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ExtensionPath)) {
    Write-Error "ERROR: Extension directory not found: $ExtensionPath"
    exit 1
}

$manifest = Join-Path $ExtensionPath "manifest.yaml"
if (-not (Test-Path $manifest)) {
    Write-Error "ERROR: manifest.yaml not found in $ExtensionPath"
    exit 1
}

Write-Host "======================================" -ForegroundColor Cy
Write-Host " GENX Extension Installer v3.6.9" -ForegroundColor Cy
Write-Host "======================================" -ForegroundColor Cy

$name = Split-Path $ExtensionPath -Leaf
$target = Join-Path "skills" $name

if (-not (Test-Path "skills")) {
    New-Item -ItemType Directory -Path "skills" -Force | Out-Null
}

if (Test-Path $target) {
    Write-Error "ERROR: Extension already exists at $target"
    exit 1
}

$requiredFiles = @("manifest.yaml", "README.md", "src", "tests", "version.txt")
foreach ($item in $requiredFiles) {
    $req = Join-Path $ExtensionPath $item
    if (-not (Test-Path $req)) {
        Write-Error "ERROR: Missing required extension component: $item"
        exit 1
    }
}

Copy-Item -Path $ExtensionPath -Destination $target -Recurse
Write-Host "`nExtension installed successfully: $target" -ForegroundColor Green
