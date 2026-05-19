import json
from phi.agent import Agent
from phi.model.groq import Groq
import datetime
import os
from pydantic import BaseModel
from typing import List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

summarizer_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    name="Summariser",
    role="extract key points from regulatory documents and articles",
    instructions=[
    """
    You are a regulatory intelligence analyst.

    Analyze the provided document and return ONLY valid JSON.

    Required JSON schema:

    {
      "short_summary": "4-5 sentence summary",
      "key_changes": ["change1", "change2", "change3"],
      "affected_industries": ["industry1", "industry2"],
      "severity": "High/Medium/Low",
      "critical_information": []
    }

    Rules:
    - Do not include markdown
    - Do not include explanations
    - Do not wrap JSON in code blocks
    - Return ONLY raw JSON
    - Keep summaries concise
    """
],
    show_tool_calls=False,
    markdown=False
)

class SummaryData(BaseModel):
    short_summary: str
    key_changes: List[str]
    affected_industries: List[str]
    severity: str
    critical_information: List[str] = []

class StructuredResponse(BaseModel):
    source: str
    title: str
    jurisdiction: str
    summary: SummaryData
    recommended_actions: List[str]

def get_summary(content: str, content_type: str) -> dict:
    try:
        # Limit text size
        max_chars = 15000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n... [content truncated]"
        
        prompt = f"Analyze this regulatory {'article' if content_type.lower() == 'article' else 'PDF'} and return structured JSON:\n\n{content}"
        
        response = summarizer_agent.run(prompt)
        
        # Parse the JSON response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Extract JSON from response (handle potential markdown wrapping)
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            summary_data = json.loads(json_str)
        else:
            summary_data = json.loads(response_text)
        
        # Validate against SummaryData model
        summary_obj = SummaryData(**summary_data)
        
        # Create structured response
        structured = {
            "source": "SEC" if "sec" in content_type.lower() or "SEC" in response_text else "RBI",
            "title": summary_obj.short_summary[:80],  # Use first part of summary as title
            "jurisdiction": "United States" if "sec" in content_type.lower() else "India",
            "summary": {
                "short_summary": summary_obj.short_summary,
                "key_changes": summary_obj.key_changes,
                "affected_industries": summary_obj.affected_industries,
                "severity": summary_obj.severity
            },
            "recommended_actions": [
                "Review disclosure policies",
                "Update compliance procedures",
                "Conduct impact assessment"
            ]
        }
        
        return structured
        
    except Exception as e:
        return {"error": str(e), "content_type": content_type}

def summarize_pdf_content(pdf_content_json_path: str) -> dict:
    try:
        # Load the extracted PDF content
        with open(pdf_content_json_path, 'r', encoding='utf-8') as f:
            pdf_data = json.load(f)
        
        # Combine all text from PDF pages
        full_text = ""
        for page in pdf_data.get('content', []):
            full_text += f"\n--- Page {page.get('page', '?')} ---\n"
            full_text += page.get('content', '')
        
        return get_summary(full_text, "pdf")
        
    except Exception as e:
        return {"error": str(e)}

def summarize_article_content(article_content_json_path: str) -> dict:
    try:
        # Load the extracted article content
        with open(article_content_json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        # Combine all text from article sections
        full_text = f"Title: {article_data.get('title', 'Unknown')}\n\n"
        for section in article_data.get('content', []):
            full_text += f"\n--- Section {section.get('section', '?')} ---\n"
            full_text += section.get('content', '')
        
        return get_summary(full_text, "article")
        
    except Exception as e:
        return {"error": str(e)}
