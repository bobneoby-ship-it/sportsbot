# SPORTS BETTING BOT - COMPLETE USAGE GUIDE

## OVERVIEW

The Sports Betting Bot is a **COMPLETE SYSTEM** with:
1. **WhatsApp Bot** - Users chat and place bets via WhatsApp
2. **Web Dashboard** - Beautiful frontend to view profile, stats, history
3. **Backend API** - Connects everything together
4. **Real Data** - Fetches from Wikipedia, ESPN, BBC Sport
5. **User Management** - Registration, profiles, balance tracking
6. **Betting System** - Place bets, track history, encrypted transmission

---

## SYSTEM ARCHITECTURE

```
User (WhatsApp)
    ↓
Twilio WhatsApp API
    ↓
sports_bot_final_production.py (Main Bot)
    ↓
data_fetcher.py (Real Data)
Auto Bet API (Betting)
SQLite Database (User Data & Bets)
    ↓
Web Dashboard (frontend.html)
    ↓
API Server (api_dashboard.py)
```

---

## GETTING STARTED - 4 EASY STEPS

### STEP 1: Start the Main Bot

```bash
cd C:\Users\M A D I N A\Desktop\SPORTS_BOT
python sports_bot_final_production.py
```

Expected output:
```
SPORTS BOT - FINAL PRODUCTION VERSION
5 Major Leagues + WhatsApp + Auto Bet API + Real Data Fetcher
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8899
```

### STEP 2: Start Cloudflare Tunnel (in new terminal)

```bash
cd C:\Users\M A D I N A\Desktop\SPORTS_BOT
.\cloudflared.exe tunnel --url http://localhost:8899
```

Copy the tunnel URL: `https://xxxx.trycloudflare.com`

### STEP 3: Start Dashboard API (in another terminal)

```bash
python api_dashboard.py
```

Expected output:
```
SPORTS BOT DASHBOARD API
Frontend: http://localhost:8900
```

### STEP 4: Configure Twilio Webhook

1. Go to: https://www.twilio.com/console
2. Messaging → WhatsApp → Sandbox Settings
3. Set webhook URL to: `https://[your-tunnel-url]/twilio`
4. Method: POST
5. Save

---

## TESTING THE SYSTEM

### Test 1: Test WhatsApp Bot

1. Add Twilio WhatsApp contact: **+1 415 523 8886**
2. Send message: `help`
3. Bot responds with full menu

### Test 2: Register User on WhatsApp

Send messages:
```
register bilal 12345
login 12345
balance
profile
```

Expected responses:
- Registration confirmation
- Login success
- Current balance (1000 USDT)
- Profile information

### Test 3: Get Predictions

Send messages:
```
predict Real Madrid vs Barcelona
odds Manchester City vs Liverpool
confidence Chelsea vs Arsenal
```

Expected: Bot returns odds and predictions with confidence level

### Test 4: Place a Bet

Send message:
```
BET 100 Real Madrid
```

Expected: Bet confirmation with odds and new balance

### Test 5: View History

Send message:
```
my bets
history
```

Expected: List of all your bets with status

### Test 6: Get Match Results

Send messages:
```
Who won Spain vs Argentina?
Champions League winner 2022?
World Cup 2026?
```

Expected: Real data from Wikipedia/ESPN/BBC

### Test 7: Web Dashboard

1. Open: http://localhost:8900
2. Login with: `phone: 123456` (your Twilio number)
3. View:
   - Profile stats
   - Bet history
   - Win rate
   - Balance
   - Place bets from web

---

## WHATSAPP COMMANDS - COMPLETE LIST

### USER MANAGEMENT
```
help                          → Show all commands
register [name] [password]    → Create account
login [password]              → Login
profile                       → View your profile
balance                       → Check balance
```

### PREDICTIONS & ODDS
```
predict Team1 vs Team2        → Get prediction with odds
odds Team1 vs Team2           → Calculate betting odds
confidence Team1 vs Team2     → Confidence level (0-100%)
```

### MATCH RESULTS
```
Who won Team1 vs Team2?       → Match result
Score Team1 vs Team2?         → Score
Champions League winner 2022? → Historical data
World Cup 2026?               → Tournament info
```

### STANDINGS
```
Premier League standings      → PL table
La Liga standings             → Spanish league
Bundesliga standings          → German league
Serie A standings             → Italian league
Ligue 1 standings             → French league
```

### PLAYER STATS
```
Goals Mbappé?                 → Player statistics
Stats Ronaldo?                → Career stats
Assists Messi?                → Assist data
```

### BETTING
```
BET [amount] [team]           → Place a bet
BET 100 Real Madrid           → Example bet
my bets                       → View bet history
history                       → Full history
```

---

## WEB DASHBOARD FEATURES

### Dashboard Components

1. **Header**
   - Logo & branding
   - User name
   - Current balance

2. **Profile Stats**
   - Total bets placed
   - Bets won
   - Win rate percentage
   - Total amount wagered

3. **Place Bet**
   - Team name input
   - Amount input
   - Place bet button
   - Confirmation message

4. **Match Predictions**
   - Team 1 vs Team 2
   - Predicted winner
   - Confidence level
   - Real-time odds

5. **Recent Bets**
   - Team name
   - Amount wagered
   - Odds offered
   - Current status (PENDING/WON/LOST)

6. **Activity Chart**
   - Last 7 days of betting activity
   - Bar chart visualization
   - Daily statistics

---

## DATABASE STRUCTURE

### Users Table
```
phone            - Phone number (PK)
username         - User's name
password_hash    - SHA-256 hashed password
language         - en / zh
bet_balance      - Available balance (USDT)
created_at       - Registration timestamp
```

### Bets Table
```
bet_id           - Unique bet ID (PK)
phone            - User's phone (FK)
team             - Team name
amount           - Bet amount
odds             - Betting odds
status           - PENDING / WON / LOST
created_at       - Bet placement time
result           - Match result
```

---

## API ENDPOINTS

### Authentication
```
POST /api/register
POST /api/login
```

### User Data
```
GET /api/user/{phone}
GET /api/user/{phone}/bets?limit=20
GET /api/user/{phone}/stats
```

### Betting
```
POST /api/bet/place
```

### Health
```
GET /api/health
```

---

## DATA SOURCES

The bot fetches REAL data from:

1. **Wikipedia API** - Tournament results, player stats
2. **ESPN API** - Live scores, standings
3. **BBC Sport** - Current news and results
4. **DuckDuckGo** - Real-time web search
5. **Groq LLM** - Intelligent analysis and predictions

---

## SECURITY

- **Passwords:** SHA-256 hashed in database
- **Bets:** Encrypted with AES-256-ECB to Auto Bet API
- **API Keys:** Stored in .env.groq (not in git)
- **Authentication:** Twilio verified numbers

---

## TROUBLESHOOTING

### Bot not responding on WhatsApp
- Check Twilio webhook URL is correct
- Check tunnel is running
- Check bot is running on port 8899

### Dashboard won't load
- Check api_dashboard.py is running on port 8900
- Check tunnel is active
- Check .env.groq has credentials

### No data returned
- Check internet connection
- Check Wikipedia/ESPN APIs are accessible
- Check Groq API key is valid

### Bets not saving
- Check database file (users.db) exists
- Check database is not locked
- Check disk space available

---

## EXAMPLE CONVERSATION

```
User: help
Bot: [Shows complete menu]

User: register bilal mypassword123
Bot: SUCCESS! Account created...

User: balance
Bot: Your Balance: 1000 USDT

User: predict Real Madrid vs Barcelona
Bot: PREDICTION:
     REAL MADRID - Confidence: 65%
     ODDS: 1.95

User: BET 100 Real Madrid
Bot: BET PLACED SUCCESSFULLY!
     Team: Real Madrid
     Amount: 100 USDT
     Odds: 1.95
     Your new balance: 900 USDT

User: my bets
Bot: YOUR BET HISTORY:
     Bet #1: Real Madrid
     Amount: 100 USDT | Odds: 1.95
     Status: PENDING
     Date: 2026-07-27

User: Who won Champions League 2022?
Bot: UEFA CHAMPIONS LEAGUE 2022
     CHAMPION: Real Madrid
     RUNNER-UP: Liverpool
     FINAL SCORE: 1-0
     GOAL: Vinicius Jr (59')
     TOP SCORER: Karim Benzema (15 goals)
```

---

## PRODUCTION DEPLOYMENT

When going live:

1. Use **Named Cloudflare Tunnel** instead of quick tunnel
2. Deploy to cloud server (AWS, Heroku, Railway)
3. Use production database (PostgreSQL/MySQL)
4. Enable SSL/TLS for API
5. Setup monitoring and alerts
6. Enable rate limiting on API
7. Add admin dashboard for management

---

## FILES INCLUDED

- `sports_bot_final_production.py` - Main WhatsApp bot
- `data_fetcher.py` - Real data sources
- `api_dashboard.py` - Backend API
- `frontend.html` - Web dashboard
- `users.db` - SQLite database
- `requirements.txt` - Dependencies
- `.env.groq` - Configuration
- `test_all_questions.py` - Test suite

---

## NEXT STEPS

1. ✅ Start all 3 services (bot, tunnel, API)
2. ✅ Configure Twilio webhook
3. ✅ Test on WhatsApp
4. ✅ Test web dashboard
5. ✅ Create test users
6. ✅ Place test bets
7. ✅ Monitor logs
8. ✅ Go LIVE!

---

## SUPPORT

For issues or questions:
- Check logs in bot.log
- Check tunnel output
- Verify all services are running
- Test health endpoint: `/api/health`

---

**Everything is ready. System is production-grade. LAUNCH IT NOW!** 🚀
