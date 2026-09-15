@echo off
REM One-Click Launcher for Jules Always-On Trading Positioning System Engine (Windows)
title Jules Always-On Trading Positioning System Engine

echo ==========================================================================
echo STARTING JULES ALWAYS-ON TRADING POSITIONING SYSTEM ENGINE
echo ==========================================================================
echo Status: ALWAYS-ON ACTIVE
echo Real-Time Market Symbol Manager: ENGAGED
echo Profit-Closing Trade Guardian: ENABLED
echo ==========================================================================

python src\main.py --always-on %*
pause
