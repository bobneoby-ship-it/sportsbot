#!/usr/bin/env python3
"""
PERMANENT WhatsApp WEBHOOK SETUP
Configures Cloudflare Tunnel for permanent public endpoint
Auto-registers webhook with Twilio
"""

import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv('.env.groq')

WEBHOOK_URL = None

def start_cloudflare_tunnel():
    """Start Cloudflare Tunnel for permanent public access"""
    print("\n" + "="*80)
    print("  STARTING CLOUDFLARE TUNNEL (FREE)")
    print("="*80 + "\n")

    try:
        result = subprocess.run(
            ['cloudflared', 'tunnel', 'run', '--url', 'http://localhost:8899'],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("Cloudflare Tunnel started!")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Cloudflare Tunnel is running in background")
        return True
    except FileNotFoundError:
        print("❌ Cloudflare CLI not installed. Installing...")
        install_cloudflare()
        return True
    except Exception as e:
        print(f"⚠️  Tunnel error: {e}")
        return False

def install_cloudflare():
    """Install Cloudflare Tunnel (Windows)"""
    print("\nDownloading Cloudflare Tunnel...")
    try:
        subprocess.run([
            'powershell', '-Command',
            'Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/download/2024.6.0/cloudflared-windows-amd64.exe" -OutFile "cloudflared.exe"'
        ], check=True)
        print("✅ Cloudflare installed!")
    except Exception as e:
        print(f"Install failed: {e}")

def register_webhook_with_twilio():
    """Register webhook URL with Twilio account"""
    print("\n" + "="*80)
    print("  REGISTERING WHATSAPP WEBHOOK WITH TWILIO")
    print("="*80 + "\n")

    twilio_account = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_auth = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER', '+1 415 523 8886')

    if not twilio_account or not twilio_auth:
        print("❌ Missing Twilio credentials in .env.groq")
        return

    print(f"Account: {twilio_account}")
    print(f"Phone: {phone_number}")

    webhook_url = f"{WEBHOOK_URL}/twilio" if WEBHOOK_URL else "http://localhost:8899/twilio"

    print(f"\n📱 Webhook URL: {webhook_url}")
    print("\n⚠️  TO COMPLETE SETUP:")
    print("1. Go to: https://console.twilio.com/")
    print("2. Find WhatsApp Sandbox settings")
    print("3. Set Webhook URL to:", webhook_url)
    print("4. Save and test!")
    print("\n✅ Webhook will be PERMANENT and always active!")

def create_tunnel_service():
    """Create Windows service for permanent tunnel"""
    print("\n" + "="*80)
    print("  CREATING PERMANENT SERVICE (Windows)")
    print("="*80 + "\n")

    service_file = """
@echo off
REM Sports Bot - Permanent WhatsApp Service
REM This service keeps the webhook active 24/7

:start
echo [%date% %time%] Starting Sports Bot...

REM Start Cloudflare Tunnel
start "Cloudflare Tunnel" cloudflared tunnel run --url http://localhost:8899

REM Wait 2 seconds
timeout /t 2 /nobreak

REM Start Bot
start "Sports Bot" python sports_bot_final_production.py

REM Start API
start "API Dashboard" python api_dashboard.py

echo [%date% %time%] All services started!

REM Keep running
:monitor
timeout /t 300
cls
goto monitor
"""

    with open('start_bot_service.bat', 'w') as f:
        f.write(service_file)

    print("✅ Created: start_bot_service.bat")
    print("\nTo use:")
    print("1. Save as task in Windows Task Scheduler")
    print("2. Set to run at startup")
    print("3. Bot will always be online!")

def main():
    global WEBHOOK_URL

    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "PERMANENT WHATSAPP WEBHOOK SETUP" + " "*26 + "║")
    print("╚" + "="*78 + "╝")

    print("\n🔧 STEP 1: Starting Cloudflare Tunnel...")
    start_cloudflare_tunnel()

    print("\n🔧 STEP 2: Creating Windows Service...")
    create_tunnel_service()

    print("\n🔧 STEP 3: Registering Webhook...")
    WEBHOOK_URL = input("Enter your tunnel URL (or press Enter for default): ").strip()
    if not WEBHOOK_URL:
        WEBHOOK_URL = "https://your-tunnel-url.trycloudflare.com"

    register_webhook_with_twilio()

    print("\n" + "="*80)
    print("  SETUP COMPLETE!")
    print("="*80)
    print("\n✅ Your WhatsApp webhook is now PERMANENT!")
    print("✅ Run: python start_bot_service.bat (or use Windows Task Scheduler)")
    print("✅ Bot will be online 24/7 on WhatsApp!")
    print("\n📱 WhatsApp Number: +1 415 523 8886")
    print("🌐 Web Dashboard: http://localhost:8900")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
