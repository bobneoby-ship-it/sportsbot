================================================================================
                 SPORTS BOT - COMPLETE PRODUCTION SYSTEM
              Auto Bet API Integration + Permanent WhatsApp Setup
================================================================================

🚀 QUICK START (ONE COMMAND):
=============================

Run: start_all_services.bat

That's it! All services start automatically.


🎮 THEN ACCESS:
================

WhatsApp:     Send message to +1 415 523 8886
Web:          http://localhost:8900
User:         test_user
Password:     password123


✨ FEATURES:
============

✅ WhatsApp Integration (PERMANENT)
   - 24/7 availability via Cloudflare Tunnel
   - Real-time message processing
   - Auto Bet API integration
   - Real data from multiple sources

✅ Web Dashboard
   - Beautiful UI with login/signup
   - Dashboard tab for statistics
   - Chat tab (just like WhatsApp)
   - Place bets, get predictions, view standings

✅ Auto Bet API Integration (REAL BETTING)
   - Sends bets to mninetoto.com
   - AES-256 encrypted payloads
   - Real ticket confirmation
   - Live balance tracking
   - Both WhatsApp AND web frontend

✅ Real Data (NO HARDCODING)
   - Wikipedia API for tournaments/teams
   - ESPN for match results
   - BBC for live data
   - DuckDuckGo for search
   - Groq LLM for analysis

✅ Sports Coverage
   - Premier League
   - La Liga
   - Bundesliga
   - Serie A
   - Ligue 1
   - Champions League
   - World Cup 2026
   - Euro 2024
   - Copa America 2024
   - Nations League

✅ Commands (Both WhatsApp & Web)
   - help → Show all commands
   - balance → Check balance
   - predict Team1 vs Team2 → Get prediction
   - BET amount Team → Place bet on Auto Bet API
   - my bets → View bet history
   - League standings → Get standings
   - Player stats → Historical/current stats
   - Tournament info → World Cup, Euro, etc.


📁 PRODUCTION FILES:
====================

FRONTEND:
- index.html ..................... Single complete web interface

BOT LOGIC:
- sports_bot_final_production.py ... WhatsApp bot (port 8899)
- api_dashboard.py ............... Web API server (port 8900)
- data_fetcher.py ............... Real data fetching engine

STARTUP:
- start_all_services.bat ......... One-click launcher
- setup_permanent_webhook.py ..... Webhook configuration

CONFIG:
- .env.groq ..................... Credentials (not in git)
- requirements.txt .............. Python dependencies

DATABASE:
- users.db ...................... User profiles & bets


🔐 YOUR AUTO BET CREDENTIALS:
==============================

Already configured in .env.groq:
- Account: mninetoto.com
- Username: kz88pggdm6
- Password: Aabbccdd8888!
- API Key: (encrypted in code)

When users place bets:
- Bot encrypts data with AES-256
- Sends to mninetoto.com
- Gets real ticket confirmation
- Tracks in database


🌍 WHATSAPP WEBHOOK (PERMANENT):
=================================

✅ Uses FREE Cloudflare Tunnel
✅ Always online - no restart needed
✅ Registered with Twilio
✅ Webhook URL: {Your Tunnel URL}/twilio

Setup is automatic in start_all_services.bat


📊 HOW IT WORKS:
=================

USER SENDS MESSAGE ON WHATSAPP:
  1. Message reaches Twilio
  2. Twilio calls bot webhook
  3. Bot processes message
  4. Bot fetches real data
  5. For bets: encrypts & sends to Auto Bet API
  6. Bot responds with results
  7. User receives reply in WhatsApp

SAME FOR WEB DASHBOARD:
  1. User types in chat or uses dashboard
  2. Frontend calls API endpoints
  3. API processes request
  4. For bets: calls Auto Bet API
  5. Results returned to frontend
  6. User sees response instantly


💰 REAL BETTING FLOW:
=====================

USER PLACES BET ($100 on Real Madrid):

WhatsApp:
- User: "BET 100 Real Madrid"
- Bot: Process → Encrypt → Send to Auto Bet API
- Bot: Receive ticket → Deduct balance → Reply with confirmation
- User: Receives ticket number & confirmation

Web Dashboard:
- User clicks "Place Bet"
- Enters: Team + Amount
- Frontend sends to API
- API encrypts & sends to Auto Bet API
- Receives ticket → Updates balance → Shows confirmation
- User sees ticket & updated balance

Both use SAME backend, SAME encryption, SAME Auto Bet API!


🎯 DEPLOYMENT OPTIONS:
======================

OPTION 1: Quick & Easy (Development)
- Run: start_all_services.bat
- Bot runs while terminal is open
- Good for testing

OPTION 2: Permanent 24/7 (Production)
- Use Windows Task Scheduler
- Bot auto-starts with Windows
- Runs even when you're not there
- See DEPLOYMENT_GUIDE.txt for details

OPTION 3: Cloud Deployment
- Deploy on cloud server (AWS, DigitalOcean, etc.)
- Keep running 24/7
- Better reliability
- Scale to many users


⚙️ SYSTEM REQUIREMENTS:
=======================

✅ Windows/Mac/Linux
✅ Python 3.8+
✅ Internet connection
✅ ~100MB disk space
✅ No external server needed (uses free Cloudflare Tunnel)


📝 DETAILED DOCS:
=================

See DEPLOYMENT_GUIDE.txt for:
- Detailed setup instructions
- Permanent 24/7 configuration
- Troubleshooting guide
- Features breakdown
- Security details
- Cost analysis


🐛 TROUBLESHOOTING:
===================

WhatsApp not responding?
- Check bot console is open
- Verify Twilio webhook in console
- Wait 2-3 seconds for response

Web dashboard won't load?
- Ensure port 8900 is available
- Check API is running in console
- Try: http://localhost:8900

Bets not placing?
- Verify .env.groq has Auto Bet credentials
- Check internet connection
- Ensure balance is sufficient
- Check team name is spelled correctly


🎓 LEARNING RESOURCES:
=====================

Code references:
- Bet encryption: sports_bot_final_production.py line 312
- Auto Bet API: sports_bot_final_production.py line 326
- Frontend betting: index.html line 734
- API endpoint: api_dashboard.py line 205


✅ YOU'RE READY!
================

1. Run: start_all_services.bat
2. Test on WhatsApp: +1 415 523 8886
3. Test on Web: http://localhost:8900
4. Set up permanent via Task Scheduler (optional)
5. Invite users!


📞 QUICK REFERENCE:
===================

Start all:      start_all_services.bat
WhatsApp:       +1 415 523 8886
Web dashboard:  http://localhost:8900
Credentials:    test_user / password123
Deployment:     DEPLOYMENT_GUIDE.txt
Issues:         Check DEPLOYMENT_GUIDE.txt "Troubleshooting"


🚀 ENJOY YOUR PRODUCTION-READY SPORTS BOT! 🚀

================================================================================
