import asyncio
import re
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from reportlab.platypus import (SimpleDocTemplate,Paragraph,Spacer)
from reportlab.lib.styles import getSampleStyleSheet

SEC_URL = "https://www.sec.gov/newsroom/press-releases"

async def get_latest_sec_article():
    async with AsyncWebCrawler() as crawler:
        # STEP 1: Crawl SEC page
        result = await crawler.arun(SEC_URL)

        if not result.html:
            print("❌ Failed to load SEC page")
            return None
        soup = BeautifulSoup(result.html, "html.parser")

        article_link = None
        article_title = None

        # STEP 3: Find first press release link
        for a in soup.find_all("a", href=True):

            href = a["href"]

            if "/newsroom/press-releases/" in href:

                article_title = a.get_text(strip=True)

                article_link = urljoin(
                    "https://www.sec.gov",
                    href
                )

                break

        if not article_link:
            print("❌ No article found")
            return None

        print(f"✓ Found article:")
        print(article_title)
        print(article_link)

        # STEP 4: Crawl article page
        article_result = await crawler.arun(article_link)

        if not article_result.html:
            print("❌ Failed to crawl article")
            return None

        article_soup = BeautifulSoup(
            article_result.html,
            "html.parser"
        )

        # STEP 5: Extract clean text
        paragraphs = article_soup.find_all("p")

        article_text = "\n\n".join(
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        return {
            "title": article_title,
            "url": article_link,
            "content": article_text
        }


def save_article_as_pdf(title, content):

    filename = re.sub(r'[^a-zA-Z0-9]+', '_', title)[:80]

    pdf_path = f"{filename}.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(title, styles['Title'])
    )

    story.append(Spacer(1, 20))

    # Content
    for para in content.split("\n\n"):

        para = para.strip()

        if para:

            story.append(
                Paragraph(
                    para,
                    styles['BodyText']
                )
            )

            story.append(Spacer(1, 10))

    doc.build(story)

    return pdf_path

async def get_latest_sec_pdf():

    article = await get_latest_sec_article()

    if not article:
        return None

    pdf_path = save_article_as_pdf(
        article["title"],
        article["content"]
    )

    filename = Path(pdf_path).name

    return {
        "pdf_path": pdf_path,
        "filename": filename,
        "title": article["title"],
        "url": article["url"]
    }

async def main():
    result = await get_latest_sec_pdf()

    if not result:
        print("❌ Failed")
        return

if __name__ == "__main__":
    asyncio.run(main())