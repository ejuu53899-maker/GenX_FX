@echo off
REM Backup USB Drive F: (U&I)
REM Simple batch wrapper for the PowerShell backup script

echo ========================================
echo   BACKUP USB DRIVE F: (U&I)
echo ========================================
echo.

cd /d "E:\.vscode\DomainController"

powershell.exe -ExecutionPolicy Bypass -File "BACKUP_USB_F.ps1"

pause
