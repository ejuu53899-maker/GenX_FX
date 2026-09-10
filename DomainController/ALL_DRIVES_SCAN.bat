@echo off
title All Drives Scan - A6_9V
color 0B

echo.
echo ========================================
echo   ALL DRIVES SCAN
echo   A6_9V Domain Controller
echo ========================================
echo.

cd /d "E:\DomainController"

powershell -ExecutionPolicy Bypass -File "ALL_DRIVES_SCAN.ps1"

pause
