#!/usr/bin/env python3
"""
REAL SPORTS DATA FETCHER - ZERO HARDCODING
Uses ONLY Free APIs with Real-Time Data
- Wikipedia API (free, no key)
- ESPN API (free, no key)
- Web Scraping (BBC Sport, ESPN)
- Groq LLM for intelligent parsing
"""

import httpx
import asyncio
from bs4 import BeautifulSoup
import logging
import re
from typing import Dict, Optional, List
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(".env.groq")
GROQ_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_KEY)

logger = logging.getLogger(__name__)

class SportsDataFetcher:
    """Fetch REAL sports data from multiple FREE sources - NO HARDCODING"""

    def __init__(self):
        self.timeout = 15
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    async def search_wikipedia_match(self, team1: str, team2: str, tournament: str = "") -> Dict:
        """Search Wikipedia for match results between two teams"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                # Search for tournament page
                query = f"{tournament} {team1} {team2}" if tournament else f"{team1} {team2}"
                url = "https://en.wikipedia.org/w/api.php"

                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json"
                }

                response = await client.get(url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    data = response.json()
                    search_results = data.get("query", {}).get("search", [])

                    if search_results:
                        # Get first result
                        first_result = search_results[0]
                        page_title = first_result.get("title", "")

                        # Fetch full page content
                        extract_params = {
                            "action": "query",
                            "titles": page_title,
                            "prop": "extracts",
                            "explaintext": True,
                            "format": "json"
                        }

                        extract_response = await client.get(url, params=extract_params, timeout=self.timeout)
                        if extract_response.status_code == 200:
                            pages = extract_response.json().get("query", {}).get("pages", {})
                            for page_id, page_data in pages.items():
                                content = page_data.get("extract", "")
                                return {
                                    "source": "Wikipedia",
                                    "page_title": page_title,
                                    "content": content,
                                    "team1": team1,
                                    "team2": team2
                                }

                return None
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return None

    async def search_espn_match(self, team1: str, team2: str) -> Dict:
        """Search ESPN for match results"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                # Try ESPN API endpoint for matches
                url = "https://site.api.espn.com/apis/site/v2/sports/soccer/matches"
                response = await client.get(url, timeout=self.timeout)

                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])

                    # Search for matching teams
                    for event in events:
                        competitors = event.get("competitors", [])
                        team_names = [c.get("team", {}).get("name", "") for c in competitors]

                        if (team1.lower() in " ".join(team_names).lower() or
                            team2.lower() in " ".join(team_names).lower()):
                            return {
                                "source": "ESPN",
                                "event": event,
                                "teams": team_names
                            }

                return None
        except Exception as e:
            logger.error(f"ESPN match search error: {e}")
            return None

    async def scrape_bbc_sport_match(self, team1: str, team2: str) -> Dict:
        """Scrape BBC Sport for match results"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                # BBC Sport search
                url = f"https://www.bbc.com/sport/football"
                response = await client.get(url, timeout=self.timeout)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Look for match results
                    match_elements = soup.find_all('div', class_='sc-4fedabbc-3')

                    results = []
                    for match in match_elements[:10]:  # Get first 10
                        text = match.get_text()
                        if team1.lower() in text.lower() or team2.lower() in text.lower():
                            results.append({
                                "source": "BBC Sport",
                                "text": text
                            })

                    return results if results else None

                return None
        except Exception as e:
            logger.error(f"BBC Sport scrape error: {e}")
            return None

    async def scrape_espn_matches(self) -> List[Dict]:
        """Scrape ESPN for live and upcoming matches"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                url = "https://www.espn.com/soccer/standings"
                response = await client.get(url, timeout=self.timeout)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    matches = []
                    # Parse match data from page
                    match_rows = soup.find_all('tr', limit=50)

                    for row in match_rows:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            matches.append({
                                "source": "ESPN Scrape",
                                "data": [cell.get_text() for cell in cells[:5]]
                            })

                    return matches[:20]  # Return first 20

                return []
        except Exception as e:
            logger.error(f"ESPN scrape error: {e}")
            return []

    async def get_match_result(self, team1: str, team2: str, tournament: str = "") -> Dict:
        """
        Get real match result between two teams
        Priority: Wikipedia > ESPN API > BBC Scrape > ESPN Scrape
        Uses Groq LLM to parse and extract actual results
        """

        logger.info(f"🔍 Fetching real match: {team1} vs {team2} ({tournament})")

        # Try Wikipedia first (most reliable for historical matches)
        wiki_data = await self.search_wikipedia_match(team1, team2, tournament)
        if wiki_data and wiki_data.get("content"):
            logger.info(f"✅ Match data from Wikipedia")
            # Use Groq to extract match result from Wikipedia content
            result = await self.parse_match_with_groq(
                wiki_data["content"],
                team1,
                team2,
                source="Wikipedia"
            )
            if result:
                return result

        # Try ESPN API
        espn_data = await self.search_espn_match(team1, team2)
        if espn_data:
            logger.info(f"✅ Match data from ESPN API")
            result = await self.parse_match_with_groq(
                str(espn_data.get("event", {})),
                team1,
                team2,
                source="ESPN API"
            )
            if result:
                return result

        # Try BBC Sport scraping
        bbc_data = await self.scrape_bbc_sport_match(team1, team2)
        if bbc_data:
            logger.info(f"✅ Match data from BBC Sport")
            for match in bbc_data:
                result = await self.parse_match_with_groq(
                    match.get("text", ""),
                    team1,
                    team2,
                    source="BBC Sport"
                )
                if result:
                    return result

        # Try ESPN scraping
        espn_matches = await self.scrape_espn_matches()
        if espn_matches:
            logger.info(f"✅ Searching ESPN Scrape data")
            for match in espn_matches:
                result = await self.parse_match_with_groq(
                    str(match.get("data", [])),
                    team1,
                    team2,
                    source="ESPN Scrape"
                )
                if result:
                    return result

        # If no data found
        return {
            "error": True,
            "message": f"Could not find match data for {team1} vs {team2}",
            "source": "No source"
        }

    async def parse_match_with_groq(self, raw_data: str, team1: str, team2: str, source: str) -> Optional[Dict]:
        """Use Groq LLM to intelligently parse match data from raw content"""
        try:
            prompt = f"""
Extract match result information from this data:

DATA: {raw_data[:2000]}

TEAMS: {team1} vs {team2}

Find and extract:
1. Final Score (Team1 Score - Team2 Score)
2. Goal Scorers (who scored and when)
3. Match Date
4. Tournament/Competition Name
5. Match Status (Finished, Live, Scheduled)

Return ONLY JSON format:
{{
    "team1": "{team1}",
    "team2": "{team2}",
    "score": "Score here",
    "team1_goals": number,
    "team2_goals": number,
    "goal_scorers": ["player1", "player2"],
    "date": "date here",
    "tournament": "tournament name",
    "status": "Finished/Live/Scheduled"
}}

If data doesn't contain match information, return empty JSON {{}}.
"""

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON from response
            import json
            try:
                # Try to find JSON in response
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    match_data = json.loads(json_match.group())
                    if match_data and match_data.get("score"):
                        match_data["source"] = source
                        return match_data
            except:
                pass

            return None
        except Exception as e:
            logger.error(f"Groq parse error: {e}")
            return None

    async def search_player_stats(self, player_name: str, tournament: str = "") -> Dict:
        """Get real player statistics from tournament"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                url = "https://en.wikipedia.org/w/api.php"

                search_params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": f"{player_name} {tournament} goals",
                    "format": "json"
                }

                response = await client.get(url, params=search_params, timeout=self.timeout)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("query", {}).get("search", [])

                    if results:
                        page_title = results[0].get("title")

                        extract_params = {
                            "action": "query",
                            "titles": page_title,
                            "prop": "extracts",
                            "explaintext": True,
                            "format": "json"
                        }

                        extract_response = await client.get(url, params=extract_params, timeout=self.timeout)
                        if extract_response.status_code == 200:
                            pages = extract_response.json().get("query", {}).get("pages", {})
                            for page_id, page_data in pages.items():
                                content = page_data.get("extract", "")

                                # Use Groq to parse stats
                                result = await self.parse_player_stats_with_groq(
                                    content,
                                    player_name,
                                    tournament
                                )
                                if result:
                                    return result

                return None
        except Exception as e:
            logger.error(f"Player stats search error: {e}")
            return None

    async def parse_player_stats_with_groq(self, content: str, player: str, tournament: str) -> Optional[Dict]:
        """Use Groq to extract player statistics"""
        try:
            prompt = f"""
Extract player statistics from this content:

CONTENT: {content[:2000]}

PLAYER: {player}
TOURNAMENT: {tournament}

Find and extract:
1. Total Goals
2. Assists
3. Matches Played
4. Goals per Match
5. Any awards (Golden Boot, etc)

Return JSON:
{{
    "player": "{player}",
    "tournament": "{tournament}",
    "goals": number,
    "assists": number,
    "matches": number,
    "goals_per_match": number,
    "awards": ["award1", "award2"]
}}

If no stats found, return {{}}.
"""

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )

            result_text = response.choices[0].message.content.strip()

            import json
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                stats = json.loads(json_match.group())
                if stats and stats.get("goals"):
                    return stats

            return None
        except Exception as e:
            logger.error(f"Groq stats parse error: {e}")
            return None

    async def search_league_standings(self, league_name: str) -> Dict:
        """Get real league standings"""
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                url = "https://en.wikipedia.org/w/api.php"

                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": f"{league_name} standings 2025 2026",
                    "format": "json"
                }

                response = await client.get(url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("query", {}).get("search", [])

                    if results:
                        page_title = results[0].get("title")

                        extract_params = {
                            "action": "query",
                            "titles": page_title,
                            "prop": "extracts",
                            "explaintext": True,
                            "format": "json"
                        }

                        extract_response = await client.get(url, params=extract_params, timeout=self.timeout)
                        if extract_response.status_code == 200:
                            pages = extract_response.json().get("query", {}).get("pages", {})
                            for page_id, page_data in pages.items():
                                content = page_data.get("extract", "")

                                return {
                                    "source": "Wikipedia",
                                    "league": league_name,
                                    "content": content[:3000]
                                }

                return None
        except Exception as e:
            logger.error(f"League standings error: {e}")
            return None


# Singleton instance
data_fetcher = SportsDataFetcher()
