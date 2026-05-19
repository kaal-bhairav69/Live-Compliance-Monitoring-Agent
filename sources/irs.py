import asyncio
import re
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

IRS_URL = "https://www.irs.gov/newsroom/news-releases-for-current-month"

async def get_latest_irs_article():
    async with AsyncWebCrawler() as crawler:
        # STEP 1: Crawl IRS page
        result = await crawler.arun(IRS_URL)

        if not result.html:
            print("❌ Failed to load IRS page")
            return None
        soup = BeautifulSoup(result.html, "html.parser")

        article_link = None
        article_title = None

        # STEP 2: Find all links and look for actual news release article titles
        # Article titles are typically much longer than nav items (60+ chars)
        article_items = soup.find_all("a", href=True)
        
        for a in article_items:
            href = a["href"]
            text = a.get_text(strip=True)
            
            # Look for longer text (actual article titles, not nav items)
            if len(text) < 60:
                continue
            
            # Make sure it's not just repeated text or special characters
            if text.count(" ") < 3:
                continue
            
            article_title = text
            # Handle both absolute and relative URLs
            if href.startswith("http"):
                article_link = href
            else:
                article_link = urljoin("https://www.irs.gov", href)
            print(f"✓ Found article: {article_title[:80]}...")
            print(f"  Link: {article_link}")
            break

        if not article_link:
            print("❌ No article found")
            print(f"Total links scanned: {len(article_items)}")
            # Print some longer links for debugging
            print("\nLinks with 30+ characters:")
            for a in article_items:
                text = a.get_text(strip=True)
                if len(text) >= 30:
                    print(f"  {text[:80]}")
            return None

        print(f"✓ Found article:")
        print(article_title)
        print(article_link)

        # STEP 3: Crawl article page
        article_result = await crawler.arun(article_link)

        if not article_result.html:
            print("❌ Failed to crawl article")
            return None

        article_soup = BeautifulSoup(
            article_result.html,
            "html.parser"
        )

        # STEP 4: Extract clean text
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

    # Save to absolute path in sources directory
    pdf_path = Path(__file__).parent / f"{filename}.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

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

    return str(pdf_path)

async def get_latest_irs_pdf():

    article = await get_latest_irs_article()

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
    result = await get_latest_irs_pdf()

    if not result:
        print("❌ Failed")
        return

if __name__ == "__main__":
    asyncio.run(main())
