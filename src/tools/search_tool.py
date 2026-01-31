"""
أداة البحث في مصادر متعددة
"""

import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup


class SearchTool:
    """أداة البحث في الويب"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def search(
        self,
        query: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """البحث في الويب"""
        session = await self._get_session()
        
        url = f"https://duckduckgo.com/html/?q={query}&kl=us-en"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                for result in soup.select('.result')[:num_results]:
                    title_elem = result.select_one('.result__title a')
                    snippet_elem = result.select_one('.result__snippet')
                    link_elem = result.select_one('.result__url')
                    
                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text(strip=True),
                            "url": link_elem.get('href', ''),
                            "snippet": snippet_elem.get_text(strip=True) if snippet_elem else '',
                            "relevance": 0.8
                        })
                
                return results
                
        except Exception as e:
            return [{"error": str(e)}]
    
    async def search_news(
        self,
        query: str,
        num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """البحث في الأخبار"""
        session = await self._get_session()
        
        url = f"https://news.google.com/search?q={query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                news = []
                for item in soup.select('article')[:num_results]:
                    title_elem = item.select_one('h3')
                    link_elem = item.select_one('a')
                    
                    if title_elem and link_elem:
                        news.append({
                            "title": title_elem.get_text(strip=True),
                            "url": f"https://news.google.com{link_elem.get('href', '')}",
                            "source": "News",
                            "relevance": 0.85
                        })
                
                return news
                
        except Exception as e:
            return [{"error": str(e)}]
    
    async def close(self):
        """إغلاق الجلسة"""
        if self.session and not self.session.closed:
            await self.session.close()
