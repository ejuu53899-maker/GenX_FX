# Backup to Dropbox
# Backs up critical files to Dropbox organized structure

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("Daily", "Weekly", "Monthly", "Critical", "All")]
    [string]$Type = "Critical"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP TO DROPBOX" -ForegroundColor Cyan
Write-Host "  Type: $Type" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Dropbox is at new location (E:) or old location (C:)
if (Test-Path "E:\Dropbox") {
    $dropboxPath = "E:\Dropbox"
} elseif (Test-Path "C:\Users\lengk\Dropbox") {
    $dropboxPath = "C:\Users\lengk\Dropbox"
} else {
    $dropboxPath = "C:\Users\lengk\Dropbox"  # Default fallback
}
$domainControllerPath = "E:\DomainController"

if (-not (Test-Path $dropboxPath)) {
    Write-Host "ERROR: Dropbox path not found: $dropboxPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

if (-not (Test-Path $domainControllerPath)) {
    Write-Host "ERROR: Domain Controller path not found: $domainControllerPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupCount = 0
$errorCount = 0

# Define backup items based on type
$backupItems = @()

switch ($Type) {
    "Critical" {
        $backupItems = @(
            @{Source = "$domainControllerPath\SecureVault"; Dest = "$dropboxPath\Credentials\SecureVault_$timestamp"; Name = "SecureVault"},
            @{Source = "$domainControllerPath\Scripts"; Dest = "$dropboxPath\DomainController\Scripts"; Name = "Scripts"},
            @{Source = "$domainControllerPath\NamecheapBackup"; Dest = "$dropboxPath\Namecheap\Account_Info"; Name = "Namecheap"},
            @{Source = "$domainControllerPath\DRIVE_CONFIG.json"; Dest = "$dropboxPath\DomainController\Configurations"; Name = "Drive Config"}
        )
    }
    "Daily" {
        $backupItems = @(
            @{Source = "$domainControllerPath\SecureVault"; Dest = "$dropboxPath\Backups\Daily\SecureVault\SecureVault_$timestamp"; Name = "SecureVault"},
            @{Source = "$domainControllerPath\*.json"; Dest = "$dropboxPath\Backups\Daily\Configurations"; Name = "Configurations"},
            @{Source = "$domainControllerPath\*.md"; Dest = "$dropboxPath\DomainController\Documentation"; Name = "Documentation"}
        )
    }
    "Weekly" {
        $backupItems = @(
            @{Source = "$domainControllerPath"; Dest = "$dropboxPath\Backups\Weekly\Full_System\DomainController_$timestamp"; Name = "Full System"},
            @{Source = "$domainControllerPath\TradingSystems"; Dest = "$dropboxPath\Trading\Backups\TradingSystems_$timestamp"; Name = "Trading Systems"}
        )
    }
    "Monthly" {
        $backupItems = @(
            @{Source = "$domainControllerPath"; Dest = "$dropboxPath\Backups\Monthly\Complete_Snapshots\DomainController_$timestamp"; Name = "Complete Snapshot"}
        )
    }
    "All" {
        $backupItems = @(
            @{Source = "$domainControllerPath\SecureVault"; Dest = "$dropboxPath\Credentials\SecureVault_$timestamp"; Name = "SecureVault"},
            @{Source = "$domainControllerPath\Scripts"; Dest = "$dropboxPath\DomainController\Scripts"; Name = "Scripts"},
            @{Source = "$domainControllerPath\NamecheapBackup"; Dest = "$dropboxPath\Namecheap\Account_Info"; Name = "Namecheap"},
            @{Source = "$domainControllerPath"; Dest = "$dropboxPath\Backups\Monthly\Complete_Snapshots\DomainController_$timestamp"; Name = "Complete System"}
        )
    }
}

Write-Host "Backing up $($backupItems.Count) item(s)..." -ForegroundColor Yellow
Write-Host ""

foreach ($item in $backupItems) {
    Write-Host "Backing up: $($item.Name)" -ForegroundColor Cyan
    Write-Host "  From: $($item.Source)" -ForegroundColor Gray
    Write-Host "  To:   $($item.Dest)" -ForegroundColor Gray

    try {
        if (Test-Path $item.Source) {
            # Create destination directory if it doesn't exist
            $destDir = Split-Path $item.Dest -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }

            # Copy files
            if (Test-Path $item.Source -PathType Container) {
                # It's a directory
                Copy-Item -Path $item.Source -Destination $item.Dest -Recurse -Force
            } else {
                # It's a file (or wildcard)
                Copy-Item -Path $item.Source -Destination $destDir -Recurse -Force
            }

            Write-Host "  [OK] Backup completed" -ForegroundColor Green
            $backupCount++
        } else {
            Write-Host "  [SKIP] Source not found" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [ERROR] $_" -ForegroundColor Red
        $errorCount++
    }

    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Successful: $backupCount" -ForegroundColor Green
Write-Host "  Errors:     $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($errorCount -eq 0) {
    Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some items could not be backed up. Please check errors above." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
