#!/usr/bin/env python3
"""
Dashboard API - Backend for web frontend
Connects frontend to user database and betting system
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from datetime import datetime
import hashlib
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "users.db"

# Models
class UserLogin(BaseModel):
    phone: str
    password: str

class BetRequest(BaseModel):
    phone: str
    team: str
    amount: float

class UserRegister(BaseModel):
    phone: str
    username: str
    password: str

# Database functions
def get_user_by_phone(phone: str):
    """Get user by phone number"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT phone, username, bet_balance, created_at FROM users WHERE phone = ?', (phone,))
        user = c.fetchone()
        conn.close()
        if user:
            return {
                "phone": user[0],
                "username": user[1],
                "balance": user[2],
                "created_at": user[3]
            }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def verify_user(phone: str, password: str) -> bool:
    """Verify user password"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT password_hash FROM users WHERE phone = ?', (phone,))
        result = c.fetchone()
        conn.close()
        if result and result[0] == password_hash:
            return True
        return False
    except:
        return False

def get_user_bets(phone: str, limit: int = 20):
    """Get user's bet history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT bet_id, team, amount, odds, status, created_at, result
                    FROM bets WHERE phone = ? ORDER BY created_at DESC LIMIT ?''',
                 (phone, limit))
        bets = c.fetchall()
        conn.close()

        return [{
            "id": bet[0],
            "team": bet[1],
            "amount": float(bet[2]),
            "odds": float(bet[3]),
            "status": bet[4],
            "date": bet[5],
            "result": bet[6]
        } for bet in bets]
    except:
        return []

def get_user_stats(phone: str):
    """Get user statistics"""
    try:
        bets = get_user_bets(phone, 100)

        total_bets = len(bets)
        won_bets = len([b for b in bets if b['status'] == 'WON'])
        lost_bets = len([b for b in bets if b['status'] == 'LOST'])
        total_wagered = sum([b['amount'] for b in bets])
        total_won = sum([b['amount'] * b['odds'] for b in bets if b['status'] == 'WON'])

        win_rate = (won_bets / total_bets * 100) if total_bets > 0 else 0

        return {
            "total_bets": total_bets,
            "won": won_bets,
            "lost": lost_bets,
            "pending": len([b for b in bets if b['status'] == 'PENDING']),
            "win_rate": round(win_rate, 2),
            "total_wagered": round(total_wagered, 2),
            "total_won": round(total_won, 2),
            "profit_loss": round(total_won - total_wagered, 2)
        }
    except:
        return None

# API Routes

@app.get("/")
async def root():
    """Serve complete dashboard frontend"""
    return FileResponse("index.html")

@app.post("/api/login")
async def login(credentials: UserLogin):
    """Login user"""
    if not verify_user(credentials.phone, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = get_user_by_phone(credentials.phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stats = get_user_stats(credentials.phone)

    return {
        "user": user,
        "stats": stats,
        "bets": get_user_bets(credentials.phone, 10)
    }

@app.post("/api/register")
async def register(data: UserRegister):
    """Register new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()

        c.execute('''INSERT INTO users (phone, username, password_hash, language, bet_balance, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (data.phone, data.username, password_hash, "en", 1000.0, datetime.now()))

        conn.commit()
        conn.close()

        user = get_user_by_phone(data.phone)
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/{phone}")
async def get_user(phone: str):
    """Get user profile"""
    user = get_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stats = get_user_stats(phone)
    bets = get_user_bets(phone, 20)

    return {
        "user": user,
        "stats": stats,
        "bets": bets
    }

@app.get("/api/user/{phone}/bets")
async def get_bets(phone: str, limit: int = 20):
    """Get user's bets"""
    bets = get_user_bets(phone, limit)
    return {"bets": bets}

@app.get("/api/user/{phone}/stats")
async def get_stats(phone: str):
    """Get user statistics"""
    stats = get_user_stats(phone)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats

@app.post("/api/bet/place")
async def place_bet(bet: BetRequest):
    """Place a bet"""
    user = get_user_by_phone(bet.phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user['balance'] < bet.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Deduct from balance
        new_balance = user['balance'] - bet.amount
        c.execute('UPDATE users SET bet_balance = ? WHERE phone = ?', (new_balance, bet.phone))

        # Record bet
        c.execute('''INSERT INTO bets (phone, team, amount, odds, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (bet.phone, bet.team, bet.amount, 1.95, 'PENDING', datetime.now()))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": "Bet placed successfully",
            "new_balance": new_balance,
            "bet": {
                "team": bet.team,
                "amount": bet.amount,
                "odds": 1.95,
                "status": "PENDING"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/bet/place-real")
async def place_real_bet(data: dict):
    """Place real bet on Auto Bet API"""
    import subprocess
    import json

    try:
        username = data.get('username')
        team = data.get('team')
        amount = data.get('amount')
        odds = data.get('odds')

        command = f'''python -c "
import sys
sys.path.insert(0, '.')
from sports_bot_final_production import place_bet_on_system
import asyncio

result = asyncio.run(place_bet_on_system('{username}', {amount}, {odds}, '1'))
print(json.dumps(result))
" 2>/dev/null'''

        result = subprocess.check_output(command, shell=True, text=True)
        bet_result = json.loads(result)

        if bet_result.get('success'):
            return {"success": True, "ticket": bet_result.get('ticket')}
        else:
            return {"success": False, "error": bet_result.get('error', 'Unknown error')}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/health")
async def health():
    """Health check"""
    return {"status": "ok", "message": "Bot API is running"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("  SPORTS BOT DASHBOARD API")
    print("  Frontend: http://localhost:8900")
    print("="*80 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8900, log_level="info")
