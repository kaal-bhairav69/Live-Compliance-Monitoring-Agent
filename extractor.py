import asyncio
import requests
import pypdf
import json
from pathlib import Path
from datetime import datetime
from webcrawl import get_content_by_source
from typing import Optional, Dict
from summarise import get_summary

async def extract_pdf_text(source):
    source_lower = source.lower()
    content_info = await get_content_by_source(source)
    
    if not content_info:
        return None
    
    pdf_url = content_info['url']
    filename = content_info['filename']
    source_name = content_info.get(
    "source",
    source.upper()
)
    
    try:
        if source_lower == 'sec' or source_lower == 'irs':
            pdf_path = pdf_url
            if not Path(pdf_path).exists():
                print(f"PDF not found at: {pdf_path}")
                return None
        else:
            response = requests.get(pdf_url, timeout=50)
            response.raise_for_status()
            pdf_path = f"temp_{filename}"
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
        
        extracted_text = []
        metadata = {}
        
        with open(pdf_path, 'rb') as f:
            pdf_reader = pypdf.PdfReader(f)
            metadata = pdf_reader.metadata
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                extracted_text.append({
                    "page": page_num,
                    "content": text.strip()
                })
        
        llm_data = {
            "source": source_name,
            "content_type": "pdf",
            "pdf_url": pdf_url,
            "filename": filename,
            "total_pages": len(extracted_text),
            "extracted_at": datetime.now().isoformat(),
            "metadata": {
                "title": str(metadata.get("/Title", "N/A")),
                "author": str(metadata.get("/Author", "N/A")),
                "created": str(metadata.get("/CreationDate", "N/A")),
            },
            "content": extracted_text
        }
        
        if source_lower != 'sec':
            Path(pdf_path).unlink()
        
        return llm_data  #maim return of the extracted content
        
    except Exception as e:
        print(e) ##error handling
        return None


def create_llm_format_json(extracted_data: dict, summary_data: dict = None) -> dict:
    source_info = {
        "filename": extracted_data.get('filename', 'unknown'),
        "url": extracted_data.get('pdf_url', 'unknown'),
        "total_pages": extracted_data.get('total_pages', 0),
        "source": extracted_data.get('source', 'Unknown')
    }
    
    final_json = {
        "timestamp": datetime.now().isoformat(),
        "source_info": {
            **source_info,
            "extracted_at": extracted_data.get('extracted_at', 'unknown'),
            "metadata": extracted_data.get('metadata', {})
        },
        #"extracted_content": extracted_data.get('content', []),
        "summary": summary_data if summary_data else None
    }
    
    return final_json


def save_final_json(final_data: dict, output_file: str = "final_content.json") -> str:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    return output_file



async def full_pipeline(source='rbi'):
    extracted_data = await extract_pdf_text(source=source)
    
    if not extracted_data:
        return None
    
    full_text = ""
    for page in extracted_data.get('content', []):
        full_text += f"\n--- Page {page.get('page')} ---\n"
        full_text += page.get('content', '')
    
    summary_data = get_summary(full_text, 'pdf')
    
    final_json = create_llm_format_json(extracted_data, summary_data)
    output_file = "sec_pdf_final.json" if source.lower() == 'sec' else "rbi_pdf_final.json"
    output_path = save_final_json(final_json, output_file)
    
    print(f"✓ Pipeline complete: {output_file}")
    return final_json

if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else 'rbi'
    final_json = asyncio.run(full_pipeline(source=source)) 

