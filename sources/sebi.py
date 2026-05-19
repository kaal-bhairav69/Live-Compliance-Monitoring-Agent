"""
SEBI Latest Circular PDF Fetcher

Fetches the single most recent SEBI circular and returns its PDF URL + filename.

Usage:
    python sebi_circulars_crawler.py

Requirements:
    pip install crawl4ai beautifulsoup4
"""

import asyncio
import re
from typing import Tuple, Optional

from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

LISTING_URL = (
    "https://www.sebi.gov.in/sebiweb/home/HomeAction.do"
    "?doListing=yes&sid=1&ssid=7&smid=0"
)
BASE_URL = "https://www.sebi.gov.in"


async def get_latest_sebi_pdf() -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (pdf_url, filename) for the latest SEBI circular.
    e.g. ("https://www.sebi.gov.in/sebi_data/attachdocs/may-2026/177824.pdf", "177824.pdf")
    """
    browser_cfg = BrowserConfig(headless=True, java_script_enabled=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:

        # Step 1: get the listing page, grab the first circular's detail URL
        listing = await crawler.arun(
            LISTING_URL,
            config=CrawlerRunConfig(wait_for="css:table", page_timeout=20_000),
        )
        if not listing.success or not listing.html:
            return None, None

        soup = BeautifulSoup(listing.html, "html.parser")
        table = soup.find("table")
        if not table:
            return None, None

        # First <a> in the table body is the latest circular
        anchor = table.find("a", href=True)
        if not anchor:
            return None, None

        detail_href = anchor["href"]
        if detail_href.startswith("/"):
            detail_href = BASE_URL + detail_href

        # Step 2: open the detail page and extract the PDF link
        detail = await crawler.arun(
            detail_href,
            config=CrawlerRunConfig(page_timeout=15_000),
        )
        if not detail.success:
            return None, None

        # PDF is embedded as: sebi_data/attachdocs/<mon-yyyy>/<id>.pdf
        pdf_match = re.search(
            r'(https?://[^\s\)"\']+sebi_data/attachdocs/[^\s\)"\']+\.pdf)',
            detail.html or "",
            re.IGNORECASE,
        )
        if pdf_match:
            pdf_url = pdf_match.group(1)
            filename = pdf_url.split("/")[-1]
            return pdf_url, filename

    return None, None


async def main():
    pdf_url, filename = await get_latest_sebi_pdf()
    if pdf_url:
        print(f"Filename : {filename}")
        print(f"URL      : {pdf_url}")
    else:
        print("Could not retrieve the latest SEBI circular PDF.")


if __name__ == "__main__":
    asyncio.run(main())