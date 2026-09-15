# GENX Command Launcher PowerShell Script
param (
    [string]$Command = "help",
    [string]$Path = ""
)

switch ($Command) {
    "start" { & .\launcher\start.sh }
    "stop" { & .\launcher\stop.sh }
    "restart" { & .\launcher\stop.sh; & .\launcher\start.sh }
    "health" { & .\launcher\health_check.sh }
    "status" { & .\launcher\health_check.sh }
    "extensions" { Get-ChildItem -Path "skills" -Filter "manifest.yaml" -Recurse }
    "install-extension" { & .\scripts\install_extension.ps1 -ExtensionPath $Path }
    "update" { & .\launcher\update.sh }
    "emergency-stop" { & .\launcher\emergency_stop.sh }
    default {
        Write-Host "GENX Starter Kit v3.6.9 Commands:"
        Write-Host "  start, stop, restart, status, health, extensions, install-extension <path>, update, emergency-stop"
    }
}
