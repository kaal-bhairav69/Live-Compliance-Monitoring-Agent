# 🚀 Getting Started Guide

A step-by-step guide to set up and run the LangGraph Multi-Agent Regulatory Intelligence System.

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** - [Download here](https://git-scm.com/)
- **A code editor** - VS Code, PyCharm, etc. (optional)

### Verify Installation

```bash
python --version  # Should be 3.8 or higher
pip --version
git --version
```

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/kaal-bhairav69/Langgraph-.git
cd Langgraph-
```

---

## Step 2: Create Virtual Environment

Virtual environments isolate project dependencies. This is **highly recommended**.

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

**Verify activation**:
```bash
# Your terminal should show: (venv) $
```

---

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This installs:
- **langgraph** - Graph orchestration
- **langchain** - LLM framework
- **phi** - Agent framework
- **groq** - LLM provider
- **pypdf** - PDF processing
- **crawl4ai** - Web crawling
- ...and more

**Verify installation**:
```bash
python -c "import langgraph; import phi; print('✅ All packages installed!')"
```

---

## Step 4: Configure Environment Variables

### Create `.env` File

```bash
cp .env.example .env
```

### Edit `.env` with Your API Keys

```env
# Get from https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional: For OpenAI integration
OPENAI_API_KEY=your_openai_api_key_here

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost:5432/regulatory_db

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

**How to get API keys**:
1. **Groq API Key**:
   - Go to [Groq Console](https://console.groq.com/)
   - Sign up or log in
   - Create API key
   - Copy to `.env`

2. **OpenAI API Key** (optional):
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Create API key
   - Add to `.env`

---

## Step 5: Run Your First Query

### Quick Test Script

Create a file `test_run.py`:

```python
import asyncio
from graph import build_graph

async def main():
    print("🚀 Starting LangGraph Multi-Agent System...")
    
    # Build graph
    graph = build_graph()
    
    # Create initial state
    initial_state = {
        "user_query": "What are the latest SEC regulations?",
        "filters": {},
        "client_impact_results": {},
        "monitoring_results": {},
        "analysis_results": {},
        "briefing": "",
        "run_client_analysis": False,
        "run_briefing": True
    }
    
    # Run workflow
    try:
        result = await graph.ainvoke(initial_state)
        
        print("\n✅ Workflow Completed!\n")
        print(f"📊 Analysis Results: {result['analysis_results']}")
        print(f"📋 Briefing: {result['briefing']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
```

### Run It

```bash
python test_run.py
```

### Expected Output

```
🚀 Starting LangGraph Multi-Agent System...

🚨 Monitoring Node Running...

🧠 Analyzing regulatory documents...

📋 Briefing Node Running...

✅ Workflow Completed!

📊 Analysis Results: {...}
📋 Briefing: "Executive summary of latest regulations..."
```

---

## Step 6: Explore the Components

### 1. Understanding the Graph

Look at `graph.py` to understand the workflow:

```python
# This file contains:
# - GraphState: State definition
# - monitoring_node(): Fetch documents
# - analysis_node(): Analyze documents
# - briefing_node(): Generate summary
# - build_graph(): Build the workflow
```

### 2. Check the Agents

Explore the agent implementations:

```bash
# Each agent is in agents/ directory
agents/
  ├── router_agent.py       # Route queries
  ├── analysis_agent.py     # Analyze documents
  ├── briefing_agent.py     # Generate summaries
  ├── client_impact_agent.py # Client analysis
  └── monitoring_agent.py   # Monitor sources
```

### 3. Review Data Sources

See how data is fetched:

```bash
# Source connectors
sources/
  ├── sec_2.py   # SEC documents
  ├── rbi.py     # RBI documents
  ├── sebi.py    # SEBI documents
  └── irs.py     # IRS documents
```

---

## Common Usage Patterns

### Pattern 1: Simple Query

```python
async def simple_query():
    graph = build_graph()
    state = {
        "user_query": "Latest banking regulations",
        # ... other required fields
    }
    result = await graph.ainvoke(state)
    return result["briefing"]
```

### Pattern 2: Jurisdiction-Specific Query

```python
async def india_specific_query():
    graph = build_graph()
    state = {
        "user_query": "Latest RBI guidelines for Indian banks",
        "filters": {
            "jurisdiction": "India",
            "topic": "banking"
        },
        # ... other fields
    }
    result = await graph.ainvoke(state)
    return result
```

### Pattern 3: Client Impact Analysis

```python
async def client_analysis():
    graph = build_graph()
    state = {
        "user_query": "Impact on fintech clients",
        "run_client_analysis": True,  # Enable client analysis
        "run_briefing": True,
        # ... other fields
    }
    result = await graph.ainvoke(state)
    return result["client_impact_results"]
```

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'langgraph'"

**Solution**: Ensure virtual environment is activated and dependencies installed

```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: "API Key not found" Error

**Solution**: Check `.env` file has correct API keys

```bash
# Verify .env exists and has GROQ_API_KEY
cat .env

# If missing, add:
echo "GROQ_API_KEY=your_key_here" >> .env
```

### Issue 3: Timeout Errors

**Solution**: Increase timeout or check API status

```python
# In .env, increase timeout
TIMEOUT=60  # Increase to 60 seconds
```

### Issue 4: PDF Extraction Fails

**Solution**: Ensure pypdf is installed

```bash
pip install pypdf --upgrade
```

---

## Next Steps

### 1. Explore Advanced Features
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Review agent implementations in `agents/`
- Understand state management in `graph.py`

### 2. Customize for Your Needs
- Modify `clients/data.json` with your client data
- Update regulatory sources in `sources/`
- Customize prompts and analysis in `summarise.py`

### 3. Integrate with Your Systems
- Build an API wrapper (see examples below)
- Connect to your database
- Set up monitoring and logging

### 4. Deploy to Production
- Containerize with Docker
- Deploy to cloud (AWS, GCP, Azure)
- Set up CI/CD pipeline

---

## Example: Building an API Endpoint

Want to expose this as an API? Here's a quick example using FastAPI:

```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_graph
import asyncio

app = FastAPI(title="Regulatory Intelligence API")

class QueryRequest(BaseModel):
    query: str
    jurisdiction: str = "USA"
    include_client_impact: bool = False

@app.post("/analyze")
async def analyze(request: QueryRequest):
    """Analyze regulatory query"""
    graph = build_graph()
    
    state = {
        "user_query": request.query,
        "filters": {"jurisdiction": request.jurisdiction},
        "client_impact_results": {},
        "monitoring_results": {},
        "analysis_results": {},
        "briefing": "",
        "run_client_analysis": request.include_client_impact,
        "run_briefing": True
    }
    
    result = await graph.ainvoke(state)
    
    return {
        "query": request.query,
        "analysis": result["analysis_results"],
        "briefing": result["briefing"],
        "client_impact": result.get("client_impact_results", {})
    }

# Run with: uvicorn api:app --reload
```

### Test the API:

```bash
# Install FastAPI
pip install fastapi uvicorn

# Run server
uvicorn api:app --reload

# Test endpoint (in another terminal)
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest SEC regulations", "jurisdiction": "USA"}'
```

---

## Performance Tips

### 1. Enable Caching
```python
# Documents are cached for 24 hours
# Located in ./cache directory
```

### 2. Use Batch Processing
```python
# Process multiple queries in parallel
tasks = [process_query(q) for q in queries]
results = await asyncio.gather(*tasks)
```

### 3. Monitor Resource Usage
```python
# Check logs in ./logs directory
# Monitor API token usage
```

---

## Learning Resources

- **LangGraph Docs**: https://python.langchain.com/docs/langgraph/
- **Groq API**: https://www.groq.com/
- **Phi Framework**: https://docs.phidata.com/
- **Python Async**: https://docs.python.org/3/library/asyncio.html

---

## Getting Help

- **Documentation**: Check [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: Open an issue on [GitHub](https://github.com/kaal-bhairav69/Langgraph-/issues)
- **Community**: Join discussions and Q&A

---

## What's Next?

Congratulations! 🎉 You've set up the LangGraph system. Now you can:

1. ✅ Process regulatory queries
2. ✅ Analyze documents with AI
3. ✅ Generate executive briefings
4. ✅ Assess client impact

**Ready to dive deeper?** Check out:
- Advanced examples in `examples/` (coming soon)
- Custom agent development guide
- Production deployment guide

---

*Happy analyzing! 📊*
