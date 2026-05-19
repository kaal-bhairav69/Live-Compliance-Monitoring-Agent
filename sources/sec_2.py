import asyncio
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from typing import Tuple, Optional, Dict
from sec import get_latest_sec_pdf as fetch_sec_pdf

async def get_latest_sec_pdf()->Tuple[Optional[str],Optional[str]]:
    result = await fetch_sec_pdf()
    if(result):
        return result['pdf_path'],result['filename']
    return None,None