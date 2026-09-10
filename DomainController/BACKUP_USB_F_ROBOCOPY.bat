@echo off
REM Backup USB Drive F: (U&I) using Robocopy
REM More reliable for large backups

echo ========================================
echo   BACKUP USB DRIVE F: (U^&I) - ROBOCOPY
echo ========================================
echo.

REM Check if F: drive exists
if not exist "F:\" (
    echo ERROR: USB drive F: not found!
    echo Please ensure the USB drive is connected and mounted.
    pause
    exit /b 1
)

REM Create backup directory
set "BACKUP_DIR=E:\.vscode\DomainController\backups"
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Create timestamped backup folder
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "timestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%"
set "BACKUP_FOLDER=%BACKUP_DIR%\USB_F_UandI_%timestamp%"

echo USB Drive: F:
echo Backup Destination: %BACKUP_FOLDER%
echo.
echo Starting backup...
echo.

REM Use robocopy for reliable backup
REM /E = copy subdirectories including empty ones
REM /COPYALL = copy all file info
REM /R:3 = retry 3 times on failure
REM /W:5 = wait 5 seconds between retries
REM /NP = no progress (faster)
REM /NDL = no directory list
REM /NFL = no file list
REM /LOG = log file

robocopy "F:\" "%BACKUP_FOLDER%" /E /COPYALL /R:3 /W:5 /NP /NDL /NFL /LOG:"%BACKUP_DIR%\BACKUP_LOG_%timestamp%.txt"

REM Check robocopy exit code
REM 0-7 are success codes, 8+ are error codes
if %ERRORLEVEL% LEQ 7 (
    echo.
    echo ========================================
    echo   BACKUP COMPLETED SUCCESSFULLY
    echo ========================================
    echo Backup location: %BACKUP_FOLDER%
    echo Log file: %BACKUP_DIR%\BACKUP_LOG_%timestamp%.txt
) else (
    echo.
    echo ========================================
    echo   BACKUP COMPLETED WITH ERRORS
    echo ========================================
    echo Exit code: %ERRORLEVEL%
    echo Please check the log file for details.
)

echo.
pause
