import asyncio
import re
from crawl4ai import AsyncWebCrawler
from typing import Tuple, Optional, Dict

async def get_latest_rbi_pdf() -> Tuple[Optional[str], Optional[str]]:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://www.rbi.org.in/scripts/NotificationUser.aspx?utm_source=chatgpt.com")
        pdf_links = re.findall(r'(https?://[^\s\)]+\.pdf)', result.markdown, re.IGNORECASE)
        
        if pdf_links:
            first_pdf = pdf_links[0]  # latest pdf
            filename = first_pdf.split('/')[-1]
            return first_pdf, filename
        else:
            return None, None