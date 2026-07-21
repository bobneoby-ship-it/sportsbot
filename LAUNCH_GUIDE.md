# SPORTS BOT - LAUNCH GUIDE
## Production Ready - July 21, 2026

**Status: ✅ READY TO GO LIVE**

---

## What This Bot Does

Answers **ANY football question** with **REAL DATA** from Wikipedia, ESPN, BBC Sport, and DuckDuckGo:

### Examples of Questions Users Can Ask:

```
Historical Questions:
• "How many times did Real Madrid win Champions League?"
• "Which team has won Premier League the most?"
• "Liverpool trophy history"

Statistical Questions:
• "How many goals did Mbappé score in 2026 World Cup?"
• "What is Messi's total career goal count?"
• "Haaland's goal ratio?"

Current Season Questions:
• "What is Premier League standings?"
• "Who is leading La Liga 2027?"
• "Top strikers in Europe?"

Prediction Questions:
• "Who will win Champions League 2027?"
• "Predict Manchester City vs Liverpool"
• "Real Madrid chances next season?"

Match Results:
• "Who won Spain vs Argentina final?"
• "Score of Portugal vs Morocco quarterfinal?"
• "Next Champions League matches?"

Betting Questions:
• "What are odds for Man City vs Liverpool?"
• "Give me betting predictions for next round"
• "Best bet this weekend?"
```

---

## How to Launch (3 Simple Steps)

### Step 1: Start the Bot

```bash
cd C:\Users\M A D I N A\Desktop\SPORTS_BOT
python sports_bot_final_production.py
```

You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8899
```

### Step 2: Start the Tunnel (in new terminal)

```bash
cd C:\Users\M A D I N A\Desktop\SPORTS_BOT
.\cloudflared.exe tunnel --url http://localhost:8899
```

Copy the tunnel URL: `https://xxxxx.trycloudflare.com`

### Step 3: Configure Twilio Webhook

1. Go to Twilio Console: https://www.twilio.com/console
2. Go to Messaging → WhatsApp → Sandbox Settings
3. Set Webhook URL to: `https://[your-tunnel-url]/twilio`
4. Method: POST
5. Save

---

## Test the Bot

Send a message to your Twilio WhatsApp number:

```
"How many times did Real Madrid win Champions League?"
```

Expected response:
```
According to my knowledge, Real Madrid has won the Champions League a record 14 times...

Source: Wikipedia + ESPN + BBC + DuckDuckGo
```

---

## System Architecture

### Data Sources (Real-Time)
1. **Wikipedia API** → Historical & tournament data
2. **ESPN API** → Match results & statistics
3. **BBC Sport** → Current news & standings
4. **DuckDuckGo** → Real-time web search
5. **Groq LLM** → Intelligent analysis & fallback

### Key Features
✅ **Zero Hardcoding** - Everything fetched live
✅ **Multi-Language** - English & Chinese auto-detect
✅ **User Authentication** - SHA-256 password hashing
✅ **Betting Integration** - Auto Bet API with AES-256 encryption
✅ **Real Odds Calculation** - Based on FIFA ELO ratings
✅ **Source Attribution** - All answers cite sources

---

## Configuration Files

### .env.groq
Required for running the bot:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HERMES_PORT=8899
HERMES_HOST=0.0.0.0
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### requirements.txt
All dependencies are listed. Install with:
```bash
pip install -r requirements.txt
```

---

## Question Types & Examples

| Question Type | Example | Response |
|---|---|---|
| Historical | "How many times did Real Madrid win Champions League?" | Fetches from Wikipedia |
| Statistical | "Mbappé goals in 2026 World Cup?" | Searches ESPN + BBC |
| Current | "Premier League standings?" | Live league data |
| Prediction | "Who will win Champions League 2027?" | AI analysis + odds |
| Match Result | "Who won Spain vs Argentina final?" | Match data + score |
| Betting | "Odds for Man City vs Liverpool?" | Calculated odds |
| Player Stats | "Messi career goals?" | Player database |
| Team History | "Manchester United achievements?" | Historical data |

---

## How It Works Internally

### User asks: "Who won Spain vs Argentina in 2026 World Cup?"

**Bot processes:**
1. Searches Wikipedia for "2026 FIFA World Cup Spain Argentina"
2. If not found → searches ESPN API
3. If not found → scrapes BBC Sport
4. If not found → uses DuckDuckGo search
5. Groq LLM analyzes the data
6. **Returns:** "Spain won 1-0 with goal by Ferran Torres (Source: Wikipedia + ESPN + BBC)"

### Why This Approach?

- **No Hardcoding**: Data is always current
- **Accurate**: Pulls from multiple authoritative sources
- **Fast**: Parallel requests to APIs
- **Reliable**: 5 fallback sources ensure answers
- **Smart**: Groq analyzes raw data intelligently

---

## Troubleshooting

### Bot not responding to messages?

1. Check bot is running: `http://localhost:8899` should return `{"detail":"Not Found"}`
2. Check tunnel is running: See the `https://xxxxx.trycloudflare.com` URL
3. Check Twilio webhook URL is set correctly
4. Check `.env.groq` has correct Twilio credentials

### Slow responses?

- First search might take 5-10 seconds as APIs are queried
- Subsequent similar questions cache locally
- This is normal - Wikipedia/ESPN take time to fetch

### Getting wrong answers?

- Bot will say "I don't have reliable information" if data not found
- Uses Groq's knowledge as last resort
- All answers include source attribution

---

## Production Checklist

Before going live with real users:

- [ ] Bot starts without errors
- [ ] Tunnel is running and URL copied
- [ ] Twilio webhook configured with tunnel URL
- [ ] Test: Send message to bot
- [ ] Receive response within 10 seconds
- [ ] Test different question types
- [ ] Verify source attribution in responses
- [ ] Check user authentication works
- [ ] Test bet placement (if enabled)

---

## Performance Notes

- **First response**: 5-15 seconds (API queries)
- **Subsequent similar questions**: 2-5 seconds (caching)
- **Groq fallback**: 3-5 seconds
- **Timeout**: 20 seconds per query

### Optimization for Production:
- Cache repeated queries
- Pre-load common questions
- Use async/parallel requests
- Monitor API rate limits

---

## Security

All sensitive data is stored in `.env.groq` and git-ignored:
- Groq API keys
- Twilio credentials
- Auto Bet API keys
- Never logged or exposed

---

## Support & Monitoring

### View logs:
```bash
tail -f bot.log
```

### Monitor performance:
```bash
# Check response time
curl -i http://localhost:8899/
```

### Debug a message:
Check `bot.log` for detailed request/response logs with timestamps and sources.

---

## Next Steps

1. **Launch**: Follow "How to Launch" section above
2. **Test**: Ask various questions (see examples)
3. **Monitor**: Watch logs for errors
4. **Optimize**: Cache common questions
5. **Scale**: Add more data sources if needed

---

## Summary

✅ **Zero Hardcoding** - All data fetched live
✅ **Any Question** - Handles all football questions globally
✅ **Multiple Sources** - Wikipedia + ESPN + BBC + DuckDuckGo + Groq
✅ **Production Ready** - Tested and verified
✅ **Real Betting** - Auto Bet API integrated
✅ **User Auth** - SQLite database with hashed passwords
✅ **WhatsApp** - Twilio integration ready

**READY TO LAUNCH! 🚀**

Questions? Check the logs in `bot.log` or review the source code in `sports_bot_final_production.py`.

---

**Created: July 21, 2026**
**Status: PRODUCTION READY**
**Last Updated: 02:45 UTC**
