import asyncio
import re
from crawl4ai import AsyncWebCrawler
from sec import get_latest_sec_pdf as fetch_sec_pdf
from typing import Tuple, Optional, Dict
from sources.sebi import get_latest_sebi_pdf
from sources.rbi import get_latest_rbi_pdf
from sources.sec_2 import fetch_sec_pdf , get_latest_sec_pdf
from sources.irs import get_latest_irs_pdf


async def get_content_by_source(source: str) -> Dict:
    if source.lower() == 'rbi':
        pdf_url, filename = await get_latest_rbi_pdf()
        if pdf_url:
            return {
                "source": "RBI",
                "type": "pdf",
                "url": pdf_url,
                "filename": filename
            }
    elif source.lower() == 'sec':
        pdf_url,filename = await get_latest_sec_pdf()
        if pdf_url:
            return {"source":"sec",
                    "type":"pdf",
                    "url":pdf_url,
                    "filename":filename
                    }
        
    elif source.lower()=="sebi":
       pdf_url,filename = await get_latest_sebi_pdf()
       if pdf_url:
          return {"source":"sebi",
                  "type":"pdf",
                  "url":pdf_url,
                  "filename":filename
                  }

    elif source.lower()=="irs":
       result = await get_latest_irs_pdf()
       pdf_url = result['pdf_path']
       filename = result['filename']
       if pdf_url:
          return {"source":"irs",
                  "type":"pdf",
                  "url":pdf_url,
                  "filename":filename
                  }

    return None

if __name__ == "__main__":
    async def main():
        print("Testing RBI PDF fetch...")
        pdf_url, filename = await get_latest_rbi_pdf()
        if pdf_url:
            print(f"RBI PDF: {filename}")
            print(f"URL: {pdf_url}\n")
        else:
            print("No RBI PDFs found\n")
        
        print("Testing SEC Article fetch...")
        pdf_path,filename = await get_latest_sec_pdf()
        if pdf_path:
         print(f"SEC PDF: {filename}")
         print(f"Path: {pdf_path}\n")
        else:
         print("No SEC PDFs found")
    
    asyncio.run(main())