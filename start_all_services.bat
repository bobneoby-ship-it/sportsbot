@echo off
REM ============================================================================
REM SPORTS BOT - START ALL SERVICES (PERMANENT)
REM ============================================================================

setlocal enabledelayedexpansion

title Sports Bot - All Services

cls
echo.
echo ============================================================================
echo                    SPORTS BOT - COMPLETE SYSTEM START
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Install Python 3.8+
    pause
    exit /b 1
)

echo [%date% %time%] Checking environment...

REM Check required files
if not exist "sports_bot_final_production.py" (
    echo ERROR: sports_bot_final_production.py not found!
    pause
    exit /b 1
)

if not exist "api_dashboard.py" (
    echo ERROR: api_dashboard.py not found!
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)

echo [%date% %time%] Killing any old Python processes...
taskkill /F /IM python.exe >nul 2>&1

echo [%date% %time%] Installing/updating dependencies...
python -m pip install -q -r requirements.txt

echo.
echo ============================================================================
echo                        STARTING SERVICES
echo ============================================================================
echo.

REM Start Cloudflare Tunnel
echo [%date% %time%] Starting Cloudflare Tunnel (FREE)...
if exist "cloudflared.exe" (
    start "Cloudflare Tunnel" cloudflared tunnel run --url http://localhost:8899
    echo                    ✅ Tunnel started (background)
) else (
    echo                    ⚠️  Cloudflare not installed (optional)
)

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start WhatsApp Bot
echo [%date% %time%] Starting WhatsApp Bot (port 8899)...
start "WhatsApp Bot" python sports_bot_final_production.py
echo                    ✅ WhatsApp Bot started

REM Start API Dashboard
echo [%date% %time%] Starting Web Dashboard API (port 8900)...
start "API Dashboard" python api_dashboard.py
echo                    ✅ Web Dashboard API started

echo.
echo ============================================================================
echo                       SERVICES RUNNING
echo ============================================================================
echo.
echo WHATSAPP:     Send message to +1 415 523 8886
echo WEB FRONTEND: http://localhost:8900
echo.
echo LOGIN DETAILS:
echo   Username: test_user
echo   Password: password123
echo.
echo ============================================================================
echo                    Press Ctrl+C to stop all services
echo ============================================================================
echo.

REM Monitor services
:monitor
timeout /t 60 >nul
goto monitor
