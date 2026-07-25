#!/usr/bin/env python3
"""
REAL SPORTS DATA FETCHER - Live API Sources Only
Wikipedia + ESPN + Web Scraping - ZERO Hardcoding
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
    """Fetch REAL sports data from Live Free APIs"""

    def __init__(self):
        self.timeout = 20
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    async def fetch_wikipedia_for_query(self, query: str) -> Optional[str]:
        """Fetch Wikipedia content for any sports query"""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                # Search Wikipedia for the query
                url = "https://en.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                    "srlimit": 5
                }

                response = await client.get(url, params=params)
                if response.status_code != 200:
                    return None

                results = response.json().get("query", {}).get("search", [])
                if not results:
                    return None

                # Get the first result's full content
                page_title = results[0].get("title")
                logger.info(f"Found Wikipedia page: {page_title}")

                # Fetch full page content
                extract_params = {
                    "action": "query",
                    "titles": page_title,
                    "prop": "extracts",
                    "explaintext": True,
                    "format": "json"
                }

                extract_response = await client.get(url, params=extract_params)
                if extract_response.status_code != 200:
                    return None

                pages = extract_response.json().get("query", {}).get("pages", {})
                for page_id, page_data in pages.items():
                    content = page_data.get("extract", "")
                    if content:
                        return content

                return None

        except Exception as e:
            logger.error(f"Wikipedia fetch error: {e}")
            return None

    async def fetch_espn_data(self, endpoint: str) -> Optional[Dict]:
        """Fetch ESPN API data"""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                url = f"https://site.api.espn.com/apis/site/v2{endpoint}"
                response = await client.get(url)

                if response.status_code == 200:
                    return response.json()

                return None

        except Exception as e:
            logger.error(f"ESPN fetch error: {e}")
            return None

    async def scrape_url(self, url: str) -> Optional[str]:
        """Scrape content from any URL"""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.get(url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    return text[:3000]  # First 3000 chars

                return None

        except Exception as e:
            logger.error(f"Scrape error: {e}")
            return None

    async def get_answer_with_groq(self, question: str, context: str = "") -> str:
        """Use Groq to answer a question with context"""
        try:
            prompt = f"""You are a professional football expert analyzing real tournament data.
Your job is to extract FACTUAL information from the provided data.

QUESTION: {question}

PROVIDED DATA/CONTEXT:
{context[:3000] if context else 'No context provided'}

INSTRUCTIONS:
1. Search the provided data for tournament results, standings, scores, team rankings
2. Look for mentions of: Champion, Winner, 1st place, 2nd place, 3rd place, Runner-up
3. Extract score information, dates, venues, goal scorers
4. Look for any tables, lists, or rankings that show team positions
5. If the data contains tournament brackets or results sections, parse them carefully
6. Be specific with numbers and team names

PROVIDE:
- Direct factual answers based on the data provided
- Do NOT say "I don't have information" if the data is present - extract it
- Quote relevant parts of the data if needed
- Be precise about rankings and scores

ANSWER THE QUESTION BASED ON THE DATA PROVIDED:"""

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Groq error: {e}")
            return f"Error fetching data: {str(e)}"

    async def google_search(self, query: str) -> Optional[str]:
        """Use DuckDuckGo or other free search to get results"""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                # Try DuckDuckGo HTML search (free, no key needed)
                url = "https://html.duckduckgo.com/"
                params = {"q": query, "t": "h_"}

                response = await client.get(url, params=params)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract search results
                    results = soup.find_all('div', class_='result')

                    text_results = []
                    for result in results[:5]:  # First 5 results
                        title = result.find('a', class_='result__a')
                        snippet = result.find('a', class_='result__snippet')

                        if title and snippet:
                            text_results.append(f"{title.get_text()}: {snippet.get_text()}")

                    if text_results:
                        return " ".join(text_results)

                return None

        except Exception as e:
            logger.error(f"Search error: {e}")
            return None

    async def answer_question(self, question: str) -> str:
        """
        Answer ANY football question using multi-source approach
        Priority: Wikipedia > ESPN > BBC > DuckDuckGo Search > Groq Knowledge
        ZERO HARDCODING - All data fetched from live sources
        """

        logger.info(f"Answering question: {question}")

        # Step 1: Try Wikipedia (MOST RELIABLE for real data)
        wiki_content = await self.fetch_wikipedia_for_query(question)
        if wiki_content and len(wiki_content) > 500:
            logger.info(f"Fetched from Wikipedia: {len(wiki_content)} chars")
            answer = await self.get_answer_with_groq(question, wiki_content)
            # If answer is good, return it
            if answer and "no reliable information" not in answer.lower():
                logger.info("Answered from Wikipedia + Groq")
                return answer

        # Step 2: Try ESPN API
        if "standings" in question.lower() or "league" in question.lower():
            espn_data = await self.fetch_espn_data("/sports/soccer/leagues")
            if espn_data:
                answer = await self.get_answer_with_groq(question, str(espn_data)[:2000])
                logger.info("Answered from ESPN API")
                return answer

        # Step 3: Try BBC Sport scraping
        bbc_content = await self.scrape_url("https://www.bbc.com/sport/football")
        if bbc_content and len(bbc_content) > 500:
            logger.info(f"Fetched from BBC Sport: {len(bbc_content)} chars")
            answer = await self.get_answer_with_groq(question, bbc_content)
            if answer and "no reliable information" not in answer.lower():
                logger.info("Answered from BBC Sport")
                return answer

        # Step 4: Try DuckDuckGo Search (FREE - no API key)
        search_results = await self.google_search(question)
        if search_results and len(search_results) > 200:
            logger.info(f"Fetched from DuckDuckGo: {len(search_results)} chars")
            answer = await self.get_answer_with_groq(question, search_results)
            if answer and "no reliable information" not in answer.lower():
                logger.info("Answered from DuckDuckGo + Groq")
                return answer

        # Step 5: Use Groq's knowledge base alone (last resort)
        logger.info("Using Groq LLM knowledge base")
        answer = await self.get_answer_with_groq(question)

        # If Groq can't answer either, tell user to search directly
        if not answer or "don't have" in answer.lower() or "unable" in answer.lower():
            return f"""I couldn't find reliable data on this through my sources (Wikipedia, ESPN, BBC Sport).

SUGGESTION: Please search Google directly for the most current information.

Sources I can access:
- Wikipedia (https://www.wikipedia.org)
- ESPN (https://www.espn.com)
- BBC Sport (https://www.bbc.com/sport/football)

Or tell me your findings and I can help analyze them!"""

        return answer

    async def get_match_result(self, team1: str, team2: str, tournament: str = "") -> Dict:
        """Get match result"""
        query = f"{team1} vs {team2} {tournament}".strip()
        answer = await self.answer_question(f"Who won {query}? What was the score?")

        return {
            "team1": team1,
            "team2": team2,
            "answer": answer,
            "source": "Wikipedia + ESPN + Groq LLM"
        }

    async def search_player_stats(self, player_name: str, tournament: str = "") -> Dict:
        """Get player statistics"""
        query = f"How many goals did {player_name} score{' in ' + tournament if tournament else ''}?"
        answer = await self.answer_question(query)

        return {
            "player": player_name,
            "tournament": tournament,
            "answer": answer,
            "source": "Wikipedia + ESPN + Groq LLM"
        }

    async def search_league_standings(self, league_name: str) -> Dict:
        """Get league standings"""
        query = f"What is the current {league_name} standings?"
        answer = await self.answer_question(query)

        return {
            "league": league_name,
            "answer": answer,
            "source": "Wikipedia + ESPN + Groq LLM"
        }


# Singleton instance
data_fetcher = SportsDataFetcher()
