@echo off
REM SPORTS BOT - Start All Services Script
REM This script starts:
REM 1. Main WhatsApp Bot (Port 8899)
REM 2. Cloudflare Tunnel
REM 3. Dashboard API (Port 8900)

echo.
echo ================================================================================
echo                    SPORTS BETTING BOT - STARTUP SCRIPT
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if cloudflared.exe exists
if not exist "cloudflared.exe" (
    echo ERROR: cloudflared.exe not found
    echo Please download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    pause
    exit /b 1
)

REM Check if .env.groq exists
if not exist ".env.groq" (
    echo ERROR: .env.groq not found
    echo Please create .env.groq with your API keys
    pause
    exit /b 1
)

echo Starting all services...
echo.

REM Terminal 1: Main Bot
echo [1/3] Starting Main WhatsApp Bot (Port 8899)...
start "Sports Bot - Main" python sports_bot_final_production.py
timeout /t 3 /nobreak

REM Terminal 2: Cloudflare Tunnel
echo [2/3] Starting Cloudflare Tunnel...
start "Sports Bot - Tunnel" cloudflared.exe tunnel --url http://localhost:8899
timeout /t 5 /nobreak

REM Terminal 3: Dashboard API
echo [3/3] Starting Dashboard API (Port 8900)...
start "Sports Bot - Dashboard" python api_dashboard.py
timeout /t 3 /nobreak

echo.
echo ================================================================================
echo                          ALL SERVICES STARTED!
echo ================================================================================
echo.
echo SERVICES RUNNING:
echo   1. Main Bot:      http://localhost:8899
echo   2. Dashboard:     http://localhost:8900
echo   3. Tunnel:        Check tunnel window for public URL
echo.
echo NEXT STEPS:
echo   1. Copy the tunnel URL from the tunnel window
echo   2. Set Twilio webhook to: https://[tunnel-url]/twilio
echo   3. Test on WhatsApp: +1 415 523 8886
echo   4. Open dashboard: http://localhost:8900
echo.
echo To stop services: Close the terminal windows
echo.
pause
