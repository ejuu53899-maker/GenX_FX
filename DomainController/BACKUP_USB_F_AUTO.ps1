# Backup USB Drive F: (U&I) - Auto Mode
# Non-interactive version that auto-confirms

param(
    [Parameter(Mandatory=$false)]
    [string]$Destination = "E:\.vscode\DomainController\backups"
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP USB DRIVE F: (U&I) - AUTO MODE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if F: drive exists
$usbDrive = "F:"
if (-not (Test-Path $usbDrive)) {
    Write-Host "ERROR: USB drive F: not found!" -ForegroundColor Red
    Write-Host "Please ensure the USB drive is connected and mounted." -ForegroundColor Yellow
    exit 1
}

# Get drive info
$driveLabel = "U&I"
try {
    $volume = Get-Volume -DriveLetter F -ErrorAction Stop
    if ($volume.FileSystemLabel) {
        $driveLabel = $volume.FileSystemLabel
    }
    $freeSpace = [math]::Round($volume.SizeRemaining / 1GB, 2)
    $totalSpace = [math]::Round($volume.Size / 1GB, 2)
    $usedSpace = [math]::Round(($volume.Size - $volume.SizeRemaining) / 1GB, 2)

    Write-Host "USB Drive Found:" -ForegroundColor Green
    Write-Host "  Drive: $usbDrive" -ForegroundColor White
    Write-Host "  Label: $driveLabel" -ForegroundColor White
    Write-Host "  Total Space: $totalSpace GB" -ForegroundColor White
    Write-Host "  Used Space:  $usedSpace GB" -ForegroundColor White
    Write-Host "  Free Space:  $freeSpace GB" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "Warning: Could not retrieve drive information" -ForegroundColor Yellow
    Write-Host ""
}

# Create destination directory if it doesn't exist
if (-not (Test-Path $Destination)) {
    Write-Host "Creating backup directory: $Destination" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

# Create timestamped backup folder
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupFolderName = "USB_F_UandI_$timestamp"
$backupPath = Join-Path $Destination $backupFolderName

Write-Host "Backup Destination: $backupPath" -ForegroundColor Cyan
Write-Host ""

# Check available space
$backupDrive = Split-Path $Destination -Qualifier
$backupVolume = Get-Volume -DriveLetter ($backupDrive.TrimEnd(':')) -ErrorAction SilentlyContinue
if ($backupVolume) {
    $availableSpace = [math]::Round($backupVolume.SizeRemaining / 1GB, 2)
    Write-Host "Available space on backup drive: $availableSpace GB" -ForegroundColor White
    Write-Host ""
}

Write-Host "Starting backup (auto-confirmed)..." -ForegroundColor Green
Write-Host ""

# Count files for progress
Write-Host "Scanning files..." -ForegroundColor Yellow
try {
    $files = Get-ChildItem -Path $usbDrive -Recurse -File -ErrorAction Stop
    $totalFiles = $files.Count
    $totalSize = ($files | Measure-Object -Property Length -Sum).Sum
    $totalSizeGB = [math]::Round($totalSize / 1GB, 2)

    Write-Host "Found $totalFiles files ($totalSizeGB GB)" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "ERROR: Could not scan files: $_" -ForegroundColor Red
    exit 1
}

# Start backup
$backupCount = 0
$errorCount = 0
$skippedCount = 0
$startTime = Get-Date

try {
    # Create backup directory
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

    # Copy files with progress
    Write-Host "Copying files..." -ForegroundColor Yellow
    $files | ForEach-Object {
        $relativePath = $_.FullName.Substring($usbDrive.Length + 1)
        $destPath = Join-Path $backupPath $relativePath
        $destDir = Split-Path $destPath -Parent

        try {
            # Create directory structure
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }

            # Copy file
            Copy-Item -Path $_.FullName -Destination $destPath -Force -ErrorAction Stop

            $backupCount++
            if ($backupCount % 100 -eq 0) {
                $percent = [math]::Round(($backupCount / $totalFiles) * 100, 1)
                Write-Host "  Progress: $backupCount / $totalFiles files ($percent%)" -ForegroundColor Gray
            }
        } catch {
            Write-Host "  [ERROR] Failed to copy: $relativePath" -ForegroundColor Red
            Write-Host "    Error: $_" -ForegroundColor DarkRed
            $errorCount++
        }
    }

    # Copy directories (empty ones)
    $directories = Get-ChildItem -Path $usbDrive -Recurse -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $directories) {
        $relativePath = $dir.FullName.Substring($usbDrive.Length + 1)
        $destPath = Join-Path $backupPath $relativePath
        if (-not (Test-Path $destPath)) {
            try {
                New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            } catch {
                # Ignore errors for directory creation
            }
        }
    }

} catch {
    Write-Host ""
    Write-Host "[ERROR] Backup failed: $_" -ForegroundColor Red
    $errorCount++
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Source:        $usbDrive ($driveLabel)" -ForegroundColor White
Write-Host "  Destination:   $backupPath" -ForegroundColor White
Write-Host "  Files copied:  $backupCount" -ForegroundColor $(if ($backupCount -gt 0) { "Green" } else { "Red" })
Write-Host "  Errors:        $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Duration:      $($duration.ToString('mm\:ss'))" -ForegroundColor White
Write-Host "  Total size:    $totalSizeGB GB" -ForegroundColor White
Write-Host ""

# Create backup info file
$infoFile = Join-Path $backupPath "BACKUP_INFO.txt"
$infoContent = @"
USB Drive Backup Information
============================
Source Drive: $usbDrive ($driveLabel)
Backup Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Backup Location: $backupPath
Files Copied: $backupCount
Errors: $errorCount
Total Size: $totalSizeGB GB
Duration: $($duration.ToString('mm\:ss'))
"@
Set-Content -Path $infoFile -Value $infoContent

# Create summary report file
$reportFile = Join-Path $Destination "BACKUP_REPORT_$timestamp.txt"
$reportContent = @"
USB Drive F: (U&I) Backup Report
================================
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

DRIVE INFORMATION
----------------
Drive Letter: $usbDrive
Drive Label: $driveLabel
Total Space: $totalSpace GB
Used Space: $usedSpace GB
Free Space: $freeSpace GB

BACKUP DETAILS
--------------
Backup Location: $backupPath
Files Copied: $backupCount
Errors: $errorCount
Total Size: $totalSizeGB GB
Duration: $($duration.ToString('mm\:ss'))

STATUS
------
$(if ($errorCount -eq 0 -and $backupCount -gt 0) { "✅ SUCCESS - Backup completed successfully" } elseif ($backupCount -gt 0) { "⚠️  PARTIAL - Backup completed with some errors" } else { "❌ FAILED - No files were copied" })
"@
Set-Content -Path $reportFile -Value $reportContent

if ($errorCount -eq 0 -and $backupCount -gt 0) {
    Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backup saved to: $backupPath" -ForegroundColor Cyan
    Write-Host "Report saved to: $reportFile" -ForegroundColor Cyan
} elseif ($backupCount -gt 0) {
    Write-Host "⚠️  Backup completed with some errors." -ForegroundColor Yellow
    Write-Host "Please review the errors above." -ForegroundColor Yellow
} else {
    Write-Host "❌ Backup failed. No files were copied." -ForegroundColor Red
}

Write-Host ""
