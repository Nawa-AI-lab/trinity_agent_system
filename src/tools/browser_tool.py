"""
أداة التصفح والتفاعل مع المواقع
"""

import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel


class BrowserTool:
    """أداة التصفح باستخدام Playwright"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.playwright = None
    
    async def __aenter__(self):
        """تهيئة المتصفح"""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            return self
        except ImportError:
            raise ImportError("يرجى تثبيت Playwright: pip install playwright")
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """إغلاق المتصفح"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_page(self, url: str) -> Dict[str, Any]:
        """جلب محتوى صفحة ويب"""
        try:
            async with self:
                page = await self.browser.new_page()
                await page.goto(url, wait_until="networkidle")
                
                content = await page.content()
                title = await page.title()
                
                text = await page.evaluate("""
                    () => {
                        document.querySelectorAll('script, style, nav, footer').forEach(el => el.remove());
                        return document.body.innerText;
                    }
                """)
                
                return {
                    "url": url,
                    "title": title,
                    "text": text[:10000],
                    "html": content[:50000]
                }
                
        except Exception as e:
            return {"error": str(e)}
    
    async def search_and_extract(
        self,
        query: str,
        search_engine: str = "google"
    ) -> Dict[str, Any]:
        """البحث واستخراج النتائج"""
        search_urls = {
            "google": f"https://www.google.com/search?q={query}",
            "duckduckgo": f"https://duckduckgo.com/?q={query}"
        }
        
        url = search_urls.get(search_engine, search_urls["google"])
        
        async with self:
            page = await self.browser.new_page()
            await page.goto(url, wait_until="networkidle")
            
            results = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('div.g');
                    return Array.from(items).slice(0, 10).map(item => ({
                        title: item.querySelector('h3')?.innerText || '',
                        url: item.querySelector('a')?.href || '',
                        snippet: item.querySelector('.VwiC3b')?.innerText || ''
                    }));
                }
            """)
            
            return {
                "query": query,
                "engine": search_engine,
                "results": results
            }
