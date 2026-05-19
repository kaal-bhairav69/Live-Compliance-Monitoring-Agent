# LangGraph Multi-Agent Compliance Monitoring System

A multi-agent compliance intelligence system built using LangGraph, LLMs, and live regulatory monitoring pipelines. The platform autonomously tracks updates from major financial regulators including SEC, RBI, SEBI, and IRS, extracts regulatory content from PDFs/articles, and converts them into structured compliance intelligence.

The system uses agentic orchestration to route queries, monitor jurisdiction-specific sources, analyze policy changes, generate executive briefings, and perform client-specific impact analysis. It can identify affected industries, estimate compliance severity, assign impact scores, and recommend operational actions for businesses.

## ⚡ Quick Start

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run
```python
import asyncio
from graph import build_graph

async def main():
    graph = build_graph()
    state = {
        "user_query": "What are latest SEC regulations?",
        "filters": {},
        "client_impact_results": {},
        "monitoring_results": {},
        "analysis_results": {},
        "briefing": "",
        "run_client_analysis": False,
        "run_briefing": True
    }
    result = await graph.ainvoke(state)
    print(result["briefing"])

asyncio.run(main())
```

## 🤖 System Components

### Agents
- **Router Agent** - Routes queries to appropriate agents
- **Monitoring Agent** - Fetches latest documents from regulatory sources
- **Analysis Agent** - Analyzes and summarizes documents
- **Briefing Agent** - Generates executive summaries
- **Client Impact Agent** - Assesses impact on client portfolios

### Data Sources
- **SEC** - US Securities regulations
- **RBI** - Indian Banking regulations
- **SEBI** - Indian Market regulations
- **IRS** - US Tax regulations

## 📁 Project Structure

```
├── graph.py                    # Main workflow orchestration
├── extractor.py               # PDF extraction
├── webcrawl.py                # Web crawling
├── summarise.py               # AI summarization
├── sec.py                     # SEC connector
│
├── agents/                    # Agent implementations
│   ├── router_agent.py
│   ├── analysis_agent.py
│   ├── briefing_agent.py
│   ├── client_impact_agent.py
│   └── monitoring_agent.py
│
├── sources/                   # Regulatory source connectors
│   ├── sec_2.py
│   ├── rbi.py
│   ├── sebi.py
│   ├── irs.py
│   └── income_tax.py
│
├── clients/data.json          # Client configuration
├── requirements.txt           # Dependencies
└── .env.example               # Environment template
```

## 🔧 Configuration

Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True
LOG_LEVEL=INFO
```

## 📊 Workflow

```
┌──────────────────────────────────────────────────────────────┐                      
│         Live Compliance Monitoring Systm                     │
└──────────────────────────────────────────────────────────────┘


                    ┌─────────────────────┐
                    │      USER INPUT     │
                    │---------------------│
                    │ Regulatory Query    │
                    │ Client Impact Query │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    LANGGRAPH ORCHESTRATION                  │
│--------------------------------------------------------------│
│ Controls agent execution flow and conditional routing        │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                        ROUTER AGENT                         │
│--------------------------------------------------------------│
│ Tech Used:                                                   │
│ • Python                                                     │
│ • LangGraph                                                  │
│ • Rule-based Intent Routing                                  │
│                                                              │
│ Responsibilities:                                            │
│ • Detect intent                                              │
│ • Extract filters                                            │
│ • Route workflow                                             │
│ • Trigger agents                                             │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                    MONITORING AGENT                         │
│--------------------------------------------------------------│
│ Tech Used:                                                   │
│ • Crawl4AI                                                   │
│ • Asyncio                                                    │
│ • Requests                                                   │
│ • Selenium-ready architecture                                │
│                                                              │
│ Sources Monitored:                                           │
│ • RBI                                                        │
│ • SEBI                                                       │
│ • SEC                                                        │
│ • IRS                                                        │
│                                                              │
│ Responsibilities:                                            │
│ • Crawl regulators                                           │
│ • Fetch new circulars                                        │
│ • Download documents                                         │
│ • Extract raw content                                        │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                    EXTRACTION PIPELINE                      │
│--------------------------------------------------------------│
│ Tech Used:                                                   │
│ • PyPDF                                                      │
│ • Regex                                                      │
│ • JSON Structuring                                           │
│                                                              │
│ Responsibilities:                                            │
│ • Parse documents                                            │
│ • Extract text                                               │
│ • Structure metadata                                         │
│ • Prepare LLM input                                          │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                     ANALYSIS AGENT                          │
│--------------------------------------------------------------│
│ Tech Used:                                                   │
│ • Groq LLM (Llama 3.3 70B)                                   │
│ • Phi Framework                                              │
│ • Pydantic Validation                                        │
│                                                              │
│ Responsibilities:                                            │
│ • Summarize regulations                                      │
│ • Detect key changes                                         │
│ • Identify industries                                        │
│ • Assign severity                                            │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│              CONDITIONAL LANGGRAPH ROUTING                  │
│--------------------------------------------------------------│
│ If Query = Regulation Update                                 │
│        → Briefing Agent                                      │
│                                                              │
│ If Query = Company/Client Impact                             │
│        → Client Impact Agent                                 │
└──────────┬───────────────────────────────────────────────────┘
           │
     ┌─────┴─────────────────────┐
     │                           │
     ▼                           ▼

┌──────────────────────┐   ┌──────────────────────────────┐
│   BRIEFING AGENT     │   │   CLIENT IMPACT AGENT       │
│----------------------│   │------------------------------│
│ Tech Used:           │   │ Tech Used:                   │
│ • Python             │   │ • Groq LLM                   │
│ • Structured Reports │   │ • Pydantic                   │
│                      │   │ • JSON Client Profiles       │
│ Responsibilities:    │   │                              │
│ • Generate briefings │   │ Responsibilities:            │
│ • Group updates      │   │ • Match regulations          │
│ • Show severity      │   │ • Calculate impact score     │
│ • Present insights   │   │ • Recommend actions          │
└──────────┬───────────┘   └──────────────┬───────────────┘
           │                               │
           └──────────────┬────────────────┘
                          ▼

┌──────────────────────────────────────────────────────────────┐
│                      FINAL OUTPUT                           │
│--------------------------------------------------------------│
│ • Regulatory Intelligence Briefing                           │
│ • Severity Analysis                                          │
│ • Affected Industries                                        │
│ • Client Impact Reports                                      │
│ • Compliance Recommendations                                 │
│ • Multi-country Monitoring                                   │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Features

- ✅ Multi-agent orchestration with LangGraph
- ✅ Autonomous document fetching & analysis
- ✅ Real-time regulatory monitoring
- ✅ AI-powered summarization
- ✅ Client portfolio impact analysis
- ✅ Async processing
- ✅ State management

## 📚 Usage Examples

### Example 1: Monitor SEC
```python
state["user_query"] = "Latest SEC regulations for financial institutions"
result = await graph.ainvoke(state)
```

### Example 2: RBI Analysis
```python
state["user_query"] = "RBI guidelines for Indian banks"
result = await graph.ainvoke(state)
```

### Example 3: Client Impact
```python
state["user_query"] = "How do new SEBI rules impact fintech clients?"
state["run_client_analysis"] = True
result = await graph.ainvoke(state)
```

## 🛠️ Requirements

- Python 3.8+
- Groq API key (free tier available)
- OpenAI API key (optional)

## 📦 Dependencies

- **langgraph** - Graph orchestration
- **langchain** - LLM framework
- **phi** - Agent framework
- **groq** - LLM provider
- **pypdf** - PDF processing
- **crawl4ai** - Web crawling

See `requirements.txt` for full list.

## 🔐 Security

- Store API keys in `.env` (never commit)
- Use environment variables for all secrets
- Review `.gitignore` for excluded files

## 🐛 Troubleshooting

**ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**API Key Error**
```bash
# Check .env has your API key
echo $GROQ_API_KEY
```

**PDF Extraction Fails**
```bash
pip install pypdf --upgrade
```

## 📖 Learn More

- [LangGraph Docs](https://python.langchain.com/docs/langgraph/)
- [Groq API](https://www.groq.com/)
- [Python Async](https://docs.python.org/3/library/asyncio.html)

## 📝 License

MIT License

## 🤝 Contributing

Feel free to fork, modify, and contribute improvements!

---

**Status**: Production Ready ✅
