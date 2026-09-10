# Backup USB Drive F: (U&I)
# Backs up the entire USB drive F: to the backups directory

param(
    [Parameter(Mandatory=$false)]
    [string]$Destination = "E:\.vscode\DomainController\backups"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BACKUP USB DRIVE F: (U&I)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if F: drive exists
$usbDrive = "F:"
if (-not (Test-Path $usbDrive)) {
    Write-Host "ERROR: USB drive F: not found!" -ForegroundColor Red
    Write-Host "Please ensure the USB drive is connected and mounted." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get drive info
try {
    $driveInfo = Get-PSDrive -Name F -ErrorAction Stop
    $driveLabel = if ($driveInfo.Description) { $driveInfo.Description } else { "U&I" }
    Write-Host "USB Drive Found:" -ForegroundColor Green
    Write-Host "  Drive: $usbDrive" -ForegroundColor White
    Write-Host "  Label: $driveLabel" -ForegroundColor White

    # Get volume info for more details
    $volume = Get-Volume -DriveLetter F -ErrorAction SilentlyContinue
    if ($volume) {
        $freeSpace = [math]::Round($volume.SizeRemaining / 1GB, 2)
        $totalSpace = [math]::Round($volume.Size / 1GB, 2)
        $usedSpace = [math]::Round(($volume.Size - $volume.SizeRemaining) / 1GB, 2)
        Write-Host "  Total Space: $totalSpace GB" -ForegroundColor White
        Write-Host "  Used Space:  $usedSpace GB" -ForegroundColor White
        Write-Host "  Free Space:  $freeSpace GB" -ForegroundColor White
    }
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

# Confirm before proceeding
Write-Host "This will copy all files from F: to:" -ForegroundColor Yellow
Write-Host "  $backupPath" -ForegroundColor White
Write-Host ""
$confirm = Read-Host "Continue with backup? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Backup cancelled." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host ""
Write-Host "Starting backup..." -ForegroundColor Green
Write-Host ""

# Count files for progress
Write-Host "Scanning files..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $usbDrive -Recurse -File -ErrorAction SilentlyContinue
$totalFiles = $files.Count
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum
$totalSizeGB = [math]::Round($totalSize / 1GB, 2)

Write-Host "Found $totalFiles files ($totalSizeGB GB)" -ForegroundColor Cyan
Write-Host ""

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

if ($errorCount -eq 0 -and $backupCount -gt 0) {
    Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backup saved to: $backupPath" -ForegroundColor Cyan
} elseif ($backupCount -gt 0) {
    Write-Host "⚠️  Backup completed with some errors." -ForegroundColor Yellow
    Write-Host "Please review the errors above." -ForegroundColor Yellow
} else {
    Write-Host "❌ Backup failed. No files were copied." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
