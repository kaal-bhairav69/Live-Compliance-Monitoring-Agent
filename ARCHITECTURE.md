# 🏗️ Architecture Documentation

## System Overview

This document provides a comprehensive overview of the LangGraph Multi-Agent Regulatory Intelligence System architecture.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                    (CLI, API, Dashboard)                        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │   LangGraph Engine   │
                    │  (State Management)  │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │   Agents    │      │    Tools    │      │   Sources   │
   ├─────────────┤      ├─────────────┤      ├─────────────┤
   │ • Router    │      │ • Extractor │      │ • SEC       │
   │ • Monitor   │      │ • Analyzer  │      │ • RBI       │
   │ • Analysis  │      │ • Formatter │      │ • SEBI      │
   │ • Briefing  │      │ • Cache     │      │ • IRS       │
   │ • Impact    │      │             │      │             │
   └─────────────┘      └─────────────┘      └─────────────┘
        │                    │                      │
        └────────────────────┼──────────────────────┘
                             ↓
                    ┌──────────────────────┐
                    │   Data & Storage     │
                    ├──────────────────────┤
                    │ • Database           │
                    │ • Cache (Redis)      │
                    │ • File System        │
                    └──────────────────────┘
```

## Component Architecture

### 1. Graph Engine (LangGraph)

**File**: `graph.py`

The core orchestration engine that:
- Defines the workflow as a directed acyclic graph (DAG)
- Manages state transitions between agents
- Handles error recovery and retries
- Maintains audit trail of agent decisions

**Key Features**:
```python
# Graph structure
class GraphState(TypedDict):
    user_query: str              # Input query
    filters: dict                # Routing filters
    client_impact_results: dict  # Client analysis
    monitoring_results: dict     # Raw documents
    analysis_results: dict       # Processed analysis
    briefing: str               # Executive summary
    run_client_analysis: bool   # Conditional flag
    run_briefing: bool          # Conditional flag
```

**Graph Flow**:
```
START
  ↓
[monitoring_node] → Fetch regulatory sources
  ↓
[analysis_node] → Analyze documents
  ↓
[briefing_node] → Generate summary
  ↓
[client_impact_node] → (Optional) Client analysis
  ↓
END
```

### 2. Agent Architecture

All agents inherit from a common pattern and communicate through shared state.

#### 2.1 Router Agent
**File**: `agents/router_agent.py`

**Responsibility**: Query classification and routing metadata generation

**Algorithm**:
```python
Input: user_query
Process:
  1. Extract keywords
  2. Identify jurisdiction (USA/India)
  3. Classify topic (banking, tax, trading, etc.)
  4. Assess severity (High/Medium/Low)
Output: filters dictionary
```

**Supported Classifications**:

| Dimension | Values |
|-----------|--------|
| Jurisdiction | USA, India |
| Topic | banking, tax, insider_trading, market_regulation |
| Severity | High, Medium, Low |

#### 2.2 Monitoring Agent
**File**: `agents/monitoring_agent.py`

**Responsibility**: Fetch latest documents from regulatory sources

**Process**:
1. Receives filters from router
2. Queries appropriate sources (SEC, RBI, SEBI, IRS)
3. Extracts document metadata
4. Returns raw documents for analysis

**Supported Sources**:
```python
{
    "SEC": async def from sources.sec_2,
    "RBI": async def from sources.rbi,
    "SEBI": async def from sources.sebi,
    "IRS": async def from sources.irs
}
```

#### 2.3 Analysis Agent
**File**: `agents/analysis_agent.py`

**Responsibility**: Process and analyze documents

**Pipeline**:
```
Raw Document
    ↓
[Text Extraction] → Extract all text from PDF
    ↓
[Normalization] → Clean and standardize text
    ↓
[AI Analysis] → Use LLM to analyze
    ↓
[Structuring] → Convert to JSON
    ↓
Structured Analysis
```

**Output Schema**:
```json
{
  "source": "SEC",
  "short_summary": "4-5 sentence summary",
  "key_changes": ["change1", "change2", ...],
  "affected_industries": ["industry1", "industry2"],
  "severity": "High/Medium/Low",
  "critical_information": [...]
}
```

#### 2.4 Briefing Agent
**File**: `agents/briefing_agent.py`

**Responsibility**: Generate executive summaries

**Features**:
- Condense analysis into 2-3 key points
- Highlight actionable items
- Generate recommendations
- Format for stakeholder review

#### 2.5 Client Impact Agent
**File**: `agents/client_impact_agent.py`

**Responsibility**: Map regulatory changes to client portfolios

**Process**:
1. Load client data from `clients/data.json`
2. Filter regulations by client's jurisdiction
3. Match industries with client business
4. Generate personalized impact report

### 3. Data Extraction Layer

#### 3.1 PDF Extraction
**File**: `extractor.py`

**Features**:
- Multi-page PDF processing
- Text normalization
- Metadata extraction
- Handles both local and remote PDFs

**Key Functions**:
```python
async def extract_pdf_text(source)
    # Extracts all text with page numbers
    # Returns: {"page": int, "content": str}

async def get_file_content(pdf_path)
    # Handles local and remote PDFs
```

#### 3.2 Web Crawling
**File**: `webcrawl.py`

**Features**:
- Crawl4AI integration
- Dynamic content loading
- Link extraction
- Metadata parsing

**Sources Router**:
```python
async def get_content_by_source(source: str) -> Dict:
    # Routes to appropriate source connector
    # Returns: {"source": str, "type": str, "url": str, "filename": str}
```

### 4. Summarization Engine

**File**: `summarise.py`

**Technology**: Groq LLM (Llama 3.3-70B) with Phi Framework

**Process**:
1. Takes raw document text
2. Sends to Groq model
3. Returns structured JSON summary
4. Validates schema compliance

**Output Schema**:
```python
{
    "short_summary": str,           # 4-5 sentences
    "key_changes": List[str],       # Major updates
    "affected_industries": List[str], # Impacted sectors
    "severity": str,                # High/Medium/Low
    "critical_information": List[str] # Important details
}
```

### 5. Data Sources Layer

Each regulatory source has dedicated connector module:

#### 5.1 SEC Connector
**File**: `sources/sec_2.py`

```python
async def fetch_sec_pdf() -> Tuple[str, str]
    # Returns: (pdf_url, filename)

async def get_latest_sec_pdf() -> Tuple[str, str]
    # Returns latest filing
```

#### 5.2 RBI Connector
**File**: `sources/rbi.py`

```python
async def get_latest_rbi_pdf() -> Tuple[str, str]
    # Fetches latest RBI guidelines
```

#### 5.3 SEBI Connector
**File**: `sources/sebi.py`

```python
async def get_latest_sebi_pdf() -> Tuple[str, str]
    # Fetches latest SEBI circular
```

#### 5.4 IRS Connector
**File**: `sources/irs.py`

```python
async def get_latest_irs_pdf() -> Tuple[str, str]
    # Fetches latest IRS ruling
```

### 6. Client Configuration Layer

**File**: `clients/data.json`

```json
{
  "clients": [
    {
      "id": "client_001",
      "name": "Client Name",
      "jurisdictions": ["USA", "India"],
      "industries": ["banking", "fintech"],
      "alert_threshold": "Medium",
      "contacts": ["email@example.com"],
      "portfolio": {
        "sec_exposure": 0.4,
        "rbi_exposure": 0.3,
        "sebi_exposure": 0.2,
        "irs_exposure": 0.1
      }
    }
  ]
}
```

## State Management

### State Flow

```
Initial State
    ↓
router_node: Extract filters
    ↓
monitoring_node: Fetch documents
{
  "monitoring_results": {
    "documents": [
      {
        "source": "SEC",
        "status": "success",
        "data": {...extracted_data...}
      }
    ]
  }
}
    ↓
analysis_node: Analyze documents
{
  "analysis_results": [
    {
      "source": "SEC",
      "short_summary": "...",
      "key_changes": [...],
      "severity": "High"
    }
  ]
}
    ↓
briefing_node: Create summary
{
  "briefing": "Executive summary..."
}
    ↓
[Optional] client_impact_node: Client analysis
{
  "client_impact_results": {
    "client_001": {
      "impact_score": 8.5,
      "recommendations": [...]
    }
  }
}
    ↓
Final State (Output)
```

## Error Handling

### Retry Strategy
```python
# Exponential backoff for API calls
MAX_RETRIES = 3
RETRY_DELAYS = [1, 2, 4]  # seconds

# Per agent error handling
try:
    result = await agent.process(data)
except SourceUnavailable:
    fallback_source = get_alternative_source()
    result = await agent.process_with_fallback(data, fallback_source)
```

### Error Recovery
- Missing source → Skip and continue
- PDF extraction fails → Log and mark as error
- LLM timeout → Return partial analysis
- Database error → Use cache

## Performance Optimization

### 1. Caching Layer
```python
# Cache analyzed documents
CACHE_DIR = "./cache"
CACHE_TTL = 3600 * 24  # 24 hours
```

### 2. Async Processing
- All I/O operations are async
- Concurrent source fetching
- Parallel document extraction

### 3. Rate Limiting
```python
MAX_REQUESTS_PER_MINUTE = 60
BATCH_SIZE = 10  # Documents per batch
```

## Deployment Architecture

### Development
```
Local Machine
    ↓
Python 3.8+
    ↓
Virtual Environment
    ↓
Local Cache & Logs
```

### Production
```
Docker Container
    ↓
Kubernetes Orchestration
    ↓
Load Balancer
    ↓
PostgreSQL Database
    ↓
Redis Cache
    ↓
S3 Storage
```

## API Integration Points

### Groq LLM
```python
from phi.model.groq import Groq

model = Groq(id="llama-3.3-70b-versatile")
```

### LangGraph State Management
```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(GraphState)
workflow.add_node("agent_name", agent_function)
workflow.add_edge("agent1", "agent2")
```

## Security Architecture

### 1. API Key Management
```python
# Environment variables only
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 2. Data Privacy
- Client data isolated per jurisdiction
- Encryption at rest for sensitive data
- Audit logging for compliance

### 3. Access Control
```python
# Client-specific filters
if user_jurisdiction == "USA":
    query_sec_and_irs()
elif user_jurisdiction == "India":
    query_rbi_and_sebi()
```

## Scalability Considerations

### Horizontal Scaling
- Stateless agent design
- Distributed state management via database
- Load-balanced API endpoints

### Vertical Scaling
- Async concurrency
- Multi-threaded PDF extraction
- GPU acceleration for LLM calls (future)

## Monitoring & Observability

### Key Metrics
- Query processing latency
- Document extraction success rate
- LLM token usage
- Cache hit rate
- Agent error rates

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Processing query: {query}")
logger.error(f"Agent failed: {error}")
```

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Advanced RAG (Retrieval Augmented Generation)
- [ ] Multi-modal analysis (images, videos)
- [ ] Predictive compliance alerts
- [ ] Integration with risk management systems
- [ ] Mobile app for alerts

---

*For implementation details, see the source code in the respective modules.*
