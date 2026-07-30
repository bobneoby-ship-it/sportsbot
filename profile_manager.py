#!/usr/bin/env python3
"""
USER PROFILE MANAGEMENT
Track user stats, bets, odds, predictions, profiles
"""

import sqlite3
from datetime import datetime
import json

class ProfileManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_tables()

    def init_tables(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            username TEXT,
            balance REAL DEFAULT 1000,
            total_bets INTEGER DEFAULT 0,
            won_bets INTEGER DEFAULT 0,
            lost_bets INTEGER DEFAULT 0,
            pending_bets INTEGER DEFAULT 0,
            total_wagered REAL DEFAULT 0,
            total_won REAL DEFAULT 0,
            win_rate REAL DEFAULT 0,
            favorite_team TEXT,
            favorite_league TEXT,
            country TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS user_bets (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            team TEXT,
            opponent TEXT,
            amount REAL,
            odds REAL,
            predicted_winner TEXT,
            confidence INTEGER,
            status TEXT,
            result TEXT,
            potential_win REAL,
            actual_win REAL,
            placed_at TIMESTAMP,
            settled_at TIMESTAMP,
            ticket_number TEXT,
            FOREIGN KEY(phone) REFERENCES user_profiles(phone)
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS user_predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            match_up TEXT,
            predicted_winner TEXT,
            confidence INTEGER,
            odds REAL,
            prediction_date TIMESTAMP,
            result TEXT,
            correct BOOLEAN,
            FOREIGN KEY(phone) REFERENCES user_profiles(phone)
        )''')

        conn.commit()
        conn.close()

    def create_profile(self, phone: str, username: str, country: str = "Unknown") -> dict:
        """Create new user profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''INSERT INTO user_profiles
                        (phone, username, country, last_active)
                        VALUES (?, ?, ?, ?)''',
                     (phone, username, country, datetime.now()))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Profile created!", "balance": 1000}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_profile(self, phone: str) -> dict:
        """Get complete user profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''SELECT phone, username, balance, total_bets, won_bets,
                                win_rate, total_wagered, favorite_team, favorite_league,
                                country, created_at FROM user_profiles
                         WHERE phone = ?''', (phone,))
            row = c.fetchone()
            conn.close()

            if row:
                return {
                    "phone": row[0],
                    "username": row[1],
                    "balance": row[2],
                    "total_bets": row[3],
                    "won_bets": row[4],
                    "win_rate": row[5],
                    "total_wagered": row[6],
                    "favorite_team": row[7],
                    "favorite_league": row[8],
                    "country": row[9],
                    "member_since": row[10],
                }
            return None
        except Exception as e:
            return None

    def get_betting_stats(self, phone: str) -> dict:
        """Get user betting statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('''SELECT total_bets, won_bets, lost_bets, pending_bets,
                                total_wagered, total_won FROM user_profiles
                         WHERE phone = ?''', (phone,))
            stats = c.fetchone()

            c.execute('''SELECT status, COUNT(*) FROM user_bets
                         WHERE phone = ? GROUP BY status''', (phone,))
            by_status = dict(c.fetchall())

            c.execute('''SELECT AVG(odds), MAX(odds), MIN(odds)
                         FROM user_bets WHERE phone = ? AND status = 'WON' ''', (phone,))
            avg_odds = c.fetchone()

            conn.close()

            if stats:
                return {
                    "total_bets": stats[0],
                    "won_bets": stats[1],
                    "lost_bets": stats[2],
                    "pending_bets": stats[3],
                    "total_wagered": stats[4],
                    "total_won": stats[5],
                    "win_rate": stats[0] > 0 and round((stats[1] / stats[0]) * 100, 2) or 0,
                    "by_status": by_status,
                    "avg_odds_won": avg_odds[0] or 0,
                    "best_odds": avg_odds[1] or 0,
                    "worst_odds": avg_odds[2] or 0,
                }
            return {}
        except Exception as e:
            return {}

    def get_recent_bets(self, phone: str, limit: int = 10) -> list:
        """Get recent bets with all details"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''SELECT bet_id, team, opponent, amount, odds,
                                predicted_winner, confidence, status, result,
                                potential_win, actual_win, placed_at, ticket_number
                         FROM user_bets WHERE phone = ?
                         ORDER BY placed_at DESC LIMIT ?''',
                     (phone, limit))

            bets = []
            for row in c.fetchall():
                bets.append({
                    "bet_id": row[0],
                    "team": row[1],
                    "opponent": row[2],
                    "amount": row[3],
                    "odds": row[4],
                    "predicted_winner": row[5],
                    "confidence": row[6],
                    "status": row[7],
                    "result": row[8],
                    "potential_win": row[9],
                    "actual_win": row[10],
                    "placed_at": row[11],
                    "ticket": row[12],
                })
            conn.close()
            return bets
        except Exception as e:
            return []

    def place_bet(self, phone: str, team: str, opponent: str, amount: float,
                  odds: float, confidence: int, ticket: str = None) -> dict:
        """Place a new bet"""
        try:
            profile = self.get_profile(phone)
            if not profile or profile["balance"] < amount:
                return {"success": False, "error": "Insufficient balance"}

            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            potential_win = amount * odds

            c.execute('''INSERT INTO user_bets
                        (phone, team, opponent, amount, odds, predicted_winner,
                         confidence, status, potential_win, placed_at, ticket_number)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (phone, team, opponent, amount, odds, team, confidence,
                      'PENDING', potential_win, datetime.now(), ticket))

            c.execute('''UPDATE user_profiles
                         SET balance = balance - ?,
                             total_bets = total_bets + 1,
                             pending_bets = pending_bets + 1,
                             total_wagered = total_wagered + ?
                         WHERE phone = ?''',
                     (amount, amount, phone))

            conn.commit()
            conn.close()

            return {
                "success": True,
                "message": "Bet placed!",
                "ticket": ticket,
                "potential_win": potential_win,
                "new_balance": profile["balance"] - amount,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def settle_bet(self, bet_id: int, result: str, actual_win: float = 0) -> dict:
        """Settle a completed bet"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('SELECT phone, amount, status FROM user_bets WHERE bet_id = ?',
                     (bet_id,))
            bet = c.fetchone()

            if not bet:
                return {"success": False, "error": "Bet not found"}

            phone, amount, status = bet

            if result == "WON":
                c.execute('''UPDATE user_bets SET status = ?, result = ?,
                             actual_win = ?, settled_at = ?
                             WHERE bet_id = ?''',
                         ('WON', result, actual_win, datetime.now(), bet_id))

                c.execute('''UPDATE user_profiles
                             SET balance = balance + ?,
                                 won_bets = won_bets + 1,
                                 pending_bets = pending_bets - 1,
                                 total_won = total_won + ?
                             WHERE phone = ?''',
                         (actual_win, actual_win, phone))

            elif result == "LOST":
                c.execute('''UPDATE user_bets SET status = ?, result = ?,
                             settled_at = ? WHERE bet_id = ?''',
                         ('LOST', result, datetime.now(), bet_id))

                c.execute('''UPDATE user_profiles
                             SET lost_bets = lost_bets + 1,
                                 pending_bets = pending_bets - 1
                             WHERE phone = ?''', (phone,))

            conn.commit()
            conn.close()
            return {"success": True, "message": f"Bet marked as {result}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_prediction_stats(self, phone: str) -> dict:
        """Get prediction accuracy stats"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('''SELECT COUNT(*), SUM(CAST(correct AS INT))
                         FROM user_predictions WHERE phone = ?''', (phone,))
            total, correct = c.fetchone()
            conn.close()

            if total and total > 0:
                accuracy = (correct / total) * 100
                return {
                    "total_predictions": total,
                    "correct_predictions": correct,
                    "accuracy_percent": round(accuracy, 2),
                }
            return {"total_predictions": 0, "correct_predictions": 0, "accuracy_percent": 0}
        except Exception as e:
            return {}

    def get_odds_summary(self, phone: str) -> dict:
        """Get odds analysis for user"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            c.execute('''SELECT AVG(odds), MAX(odds), MIN(odds), COUNT(*)
                         FROM user_bets WHERE phone = ?''', (phone,))
            avg, max_o, min_o, total = c.fetchone()
            conn.close()

            return {
                "average_odds": round(avg, 2) if avg else 0,
                "highest_odds_bet": max_o or 0,
                "lowest_odds_bet": min_o or 0,
                "total_bets": total or 0,
            }
        except Exception as e:
            return {}

    def get_full_profile(self, phone: str) -> dict:
        """Get complete profile with all stats"""
        profile = self.get_profile(phone)
        if not profile:
            return None

        return {
            "profile": profile,
            "betting_stats": self.get_betting_stats(phone),
            "recent_bets": self.get_recent_bets(phone, 5),
            "prediction_stats": self.get_prediction_stats(phone),
            "odds_summary": self.get_odds_summary(phone),
        }
