# Scan All Drives for Domain Controller and System Status
# Run as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ALL DRIVES SCAN" -ForegroundColor Cyan
Write-Host "  A6_9V Domain Controller" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Drive Configuration
# C, G, H: Path-only access (for file references, not scanning)
# D, E, F: Full scan and operations
$scanDrives = @('D', 'E', 'F')  # Drives to scan and run operations on
$pathOnlyDrives = @('C', 'G', 'H')  # Drives for path access only (not scanned)

Write-Host "Drive Configuration:" -ForegroundColor Cyan
Write-Host "  Scan & Operations: $($scanDrives -join ', '):" -ForegroundColor Green
Write-Host "  Path Access Only: $($pathOnlyDrives -join ', '): (for file references)" -ForegroundColor Yellow
Write-Host ""

# Get drives to scan
$drives = Get-PSDrive -PSProvider FileSystem | Where-Object {
    $_.Name -match '^[A-Z]$' -and $scanDrives -contains $_.Name
}

Write-Host "Scanning operational drives: $($scanDrives -join ', '):" -ForegroundColor Yellow
Write-Host ""

$results = @()

foreach ($drive in $drives) {
    $driveLetter = $drive.Name
    $drivePath = "$driveLetter`:\"

    Write-Host "Drive $driveLetter`:" -ForegroundColor Cyan
    Write-Host "-" * 40 -ForegroundColor Gray

    # Check if drive exists and is accessible
    if (Test-Path $drivePath) {
        try {
            # Get drive info
            $driveInfo = Get-PSDrive $driveLetter
            $freeSpace = [math]::Round($driveInfo.Free / 1GB, 2)
            $usedSpace = [math]::Round(($driveInfo.Used / 1GB), 2)
            $totalSpace = [math]::Round(($driveInfo.Free + $driveInfo.Used) / 1GB, 2)
            $percentFree = [math]::Round(($driveInfo.Free / ($driveInfo.Free + $driveInfo.Used)) * 100, 1)

            Write-Host "  Status: Available" -ForegroundColor Green
            Write-Host "  Total Space: $totalSpace GB" -ForegroundColor White
            Write-Host "  Used Space: $usedSpace GB" -ForegroundColor White
            Write-Host "  Free Space: $freeSpace GB ($percentFree%)" -ForegroundColor $(if ($percentFree -lt 10) { "Red" } elseif ($percentFree -lt 20) { "Yellow" } else { "Green" })

            # Check for Domain Controller
            $domainControllerPath = "$drivePath\DomainController"
            if (Test-Path $domainControllerPath) {
                Write-Host "  Domain Controller: [OK] Found" -ForegroundColor Green

                # Check key components
                $components = @{
                    "SecureVault" = "$domainControllerPath\SecureVault"
                    "TradingSystems" = "$domainControllerPath\TradingSystems"
                    "Scripts" = "$domainControllerPath\Scripts"
                    "Logs" = "$domainControllerPath\Logs"
                }

                Write-Host "  Components:" -ForegroundColor Yellow
                foreach ($component in $components.GetEnumerator()) {
                    if (Test-Path $component.Value) {
                        Write-Host "    [OK] $($component.Key)" -ForegroundColor Green
                    } else {
                        Write-Host "    [X] $($component.Key) - Missing" -ForegroundColor Red
                    }
                }

                # Check for startup script
                $startupScript = "$domainControllerPath\START_HEAD_DOMAIN.bat"
                if (Test-Path $startupScript) {
                    Write-Host "  Startup Script: [OK] Available" -ForegroundColor Green
                }
            } else {
                Write-Host "  Domain Controller: [X] Not Found" -ForegroundColor Yellow
            }

            # Check for other important folders
            $importantFolders = @(
                "Program Files",
                "Program Files (x86)",
                "Users",
                "Windows"
            )

            $foundFolders = @()
            foreach ($folder in $importantFolders) {
                if (Test-Path "$drivePath$folder") {
                    $foundFolders += $folder
                }
            }

            if ($foundFolders.Count -gt 0) {
                Write-Host "  System Folders: $($foundFolders -join ', ')" -ForegroundColor Cyan
            }

            $results += [PSCustomObject]@{
                Drive = $driveLetter
                Status = "Available"
                TotalSpace = "$totalSpace GB"
                FreeSpace = "$freeSpace GB"
                PercentFree = "$percentFree%"
                DomainController = if (Test-Path $domainControllerPath) { "Yes" } else { "No" }
            }

        } catch {
            Write-Host "  Status: Error accessing drive - $_" -ForegroundColor Red
            $results += [PSCustomObject]@{
                Drive = $driveLetter
                Status = "Error"
                TotalSpace = "N/A"
                FreeSpace = "N/A"
                PercentFree = "N/A"
                DomainController = "N/A"
            }
        }
    } else {
        Write-Host "  Status: Not accessible" -ForegroundColor Red
        $results += [PSCustomObject]@{
            Drive = $driveLetter
            Status = "Not Accessible"
            TotalSpace = "N/A"
            FreeSpace = "N/A"
            PercentFree = "N/A"
            DomainController = "N/A"
        }
    }

    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SCAN SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$results | Format-Table -AutoSize

Write-Host ""

# Path-Only Drives Info
Write-Host "Path-Only Drives (C:, G:, H:):" -ForegroundColor Cyan
Write-Host "  - These drives are NOT scanned for operations" -ForegroundColor Yellow
Write-Host "  - Used only for file path references when projects need files" -ForegroundColor Yellow
Write-Host "  - Common paths:" -ForegroundColor White
Write-Host "    C: - System files, user folders" -ForegroundColor Gray
Write-Host "    G: - Google Drive" -ForegroundColor Gray
Write-Host "    H: - Google Drive (My Drive), trading systems" -ForegroundColor Gray
Write-Host ""

# Recommendations
Write-Host "Recommendations:" -ForegroundColor Yellow
$domainControllerDrives = $results | Where-Object { $_.DomainController -eq "Yes" }
if ($domainControllerDrives.Count -eq 0) {
    Write-Host "  - No Domain Controller found on any operational drive" -ForegroundColor Red
    Write-Host "  - Consider deploying to Drive D:, E:, or F:" -ForegroundColor Yellow
} elseif ($domainControllerDrives.Count -eq 1) {
    Write-Host "  - Domain Controller found on Drive $($domainControllerDrives.Drive):" -ForegroundColor Green
    Write-Host "  - Consider deploying to additional drives (D:, F:) for redundancy" -ForegroundColor Yellow
} else {
    Write-Host "  - Domain Controller found on $($domainControllerDrives.Count) drive(s)" -ForegroundColor Green
    Write-Host "  - Good redundancy setup" -ForegroundColor Green
}

$lowSpaceDrives = $results | Where-Object {
    $_.PercentFree -ne "N/A" -and [double]($_.PercentFree -replace '%', '') -lt 10
}
if ($lowSpaceDrives.Count -gt 0) {
    Write-Host "  - Low space warning on: $($lowSpaceDrives.Drive -join ', ')" -ForegroundColor Red
    Write-Host "  - Consider cleaning up or expanding storage" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Deploy Domain Controller to additional drives: DEPLOY_TO_ALL_DRIVES.bat" -ForegroundColor White
Write-Host "  2. Run Domain Controller on specific drive: RUN_DRIVES_D_THEN_F.bat" -ForegroundColor White
Write-Host "  3. Check drive health: MONITOR_ALL_DRIVES.bat" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
