@echo off
REM Add ProtonMail and Wallet Credentials
REM Quick launcher

echo.
echo ============================================================================
echo   ADDING PROTONMAIL AND WALLET CREDENTIALS
echo ============================================================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0ADD_PROTON_CREDENTIALS.ps1"

pause
