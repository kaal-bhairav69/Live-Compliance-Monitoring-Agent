# 🤝 Contributing Guidelines

Thank you for your interest in contributing to the LangGraph Multi-Agent Regulatory Intelligence System! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and constructive
- Welcome different perspectives and experiences
- Report inappropriate behavior

---

## Ways to Contribute

### 1. Report Bugs 🐛
Found a bug? Please report it!

**How to report**:
1. Go to [Issues](https://github.com/kaal-bhairav69/Langgraph-/issues)
2. Click "New Issue"
3. Provide:
   - Clear title describing the bug
   - Detailed description of the issue
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version and OS

**Example**:
```
Title: PDF extraction fails for SEC documents

Description:
When processing SEC filings, the PDF extraction fails with Unicode errors.

Steps to reproduce:
1. Run with SEC query
2. Observe error in logs
3. See attached error trace

Expected: Clean text extraction
Actual: UnicodeDecodeError on page 3
```

### 2. Suggest Features 💡
Have an idea to improve the system?

**How to suggest**:
1. Go to [Issues](https://github.com/kaal-bhairav69/Langgraph-/issues)
2. Click "New Issue" → "Feature request"
3. Provide:
   - Clear title
   - Detailed description
   - Use case and benefits
   - Possible implementation approach

**Example**:
```
Title: Add REST API endpoint for bulk queries

Description:
Users need to submit multiple queries without waiting for each to complete.

Proposed API:
POST /api/v1/batch-analyze
{
  "queries": ["query1", "query2"],
  "jurisdiction": "USA"
}

Benefits:
- Support batch processing
- Reduce integration complexity
- Enable asynchronous workflows
```

### 3. Improve Documentation 📚
Help improve README, guides, and code comments

**How to contribute**:
1. Identify documentation gaps
2. Fork the repository
3. Make improvements
4. Submit a pull request

**Documentation to improve**:
- README.md - Main project overview
- ARCHITECTURE.md - System design
- GETTING_STARTED.md - Setup guide
- Inline code comments

### 4. Submit Code Changes 💻

**Major contributions welcome**:
- New agents or tools
- Additional data sources (SEC, RBI, etc.)
- Performance optimizations
- Bug fixes
- Tests

---

## Development Setup

### 1. Fork the Repository

Click "Fork" on the GitHub repo to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Langgraph-.git
cd Langgraph-
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# Example: git checkout -b feature/add-twitter-source
```

**Branch naming conventions**:
- `feature/description` - New feature
- `bugfix/description` - Bug fix
- `docs/description` - Documentation
- `test/description` - Tests

### 4. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # (optional) dev tools
```

### 5. Make Your Changes

```bash
# Edit files
# Test your changes
python test_run.py

# Commit changes
git add .
git commit -m "Add feature: description"
```

**Commit message conventions**:
```
[TYPE] Description

More detailed explanation if needed.

Fixes #123 (if fixing an issue)
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request

1. Go to GitHub repo
2. Click "Compare & pull request"
3. Fill in PR template:

```markdown
## Description
What changes does this PR make?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

---

## Code Style Guide

### Python Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some additions:

**Imports**:
```python
# Standard library
import asyncio
import json

# Third-party
from pydantic import BaseModel
from langchain import ...

# Local
from agents import BaseAgent
```

**Function Naming**:
```python
# Good
async def process_query(query: str) -> Dict[str, Any]:
    """Process a user query and return analysis results."""
    pass

# Bad
async def pq(q):
    pass
```

**Docstrings**:
```python
def analyze_document(doc: str, include_keywords: bool = True) -> Dict:
    """
    Analyze a document and extract key information.
    
    Args:
        doc: Document text to analyze
        include_keywords: Whether to extract keywords (default: True)
        
    Returns:
        Dictionary with analysis results including:
        - summary: Document summary
        - keywords: Extracted keywords (if include_keywords=True)
        - entities: Named entities
        
    Example:
        >>> result = analyze_document("Document text here")
        >>> print(result["summary"])
    """
    pass
```

**Type Hints**:
```python
from typing import Dict, List, Optional, Any

# Good
def process_data(data: List[Dict[str, Any]]) -> Dict[str, float]:
    pass

# Bad
def process_data(data):
    pass
```

### Formatting Tools

Use these tools to maintain consistency:

```bash
# Format code with Black
black .

# Check style with Flake8
flake8 .

# Check types with MyPy
mypy .

# Sort imports with isort
isort .
```

---

## Testing Requirements

### Write Tests for New Code

```python
# tests/test_my_agent.py
import pytest
from agents.my_agent import MyAgent

@pytest.mark.asyncio
async def test_agent_initialization():
    agent = MyAgent()
    assert agent.name == "my_agent"

@pytest.mark.asyncio
async def test_agent_process():
    agent = MyAgent()
    result = await agent.process("test query")
    assert "response" in result
    assert result["success"] is True
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_my_agent.py

# Run with coverage
pytest tests/ --cov

# Run with verbose output
pytest tests/ -v
```

### Coverage Requirements

- Minimum 70% code coverage
- All public methods should have tests
- Edge cases should be tested

---

## Documentation Standards

### README Updates

If your change affects usage, update:
- Features section (new capabilities)
- Usage section (new examples)
- Configuration (new settings)
- Troubleshooting (new issues)

### Code Comments

```python
# Good - explains WHY
# Filter results to exclude low-confidence items
# as they often produce false positives
results = [r for r in results if r.confidence > 0.8]

# Bad - explains WHAT (code already shows that)
# Filter results
results = [r for r in results if r.confidence > 0.8]
```

### Docstring Format

Use Google-style docstrings:

```python
def my_function(arg1: str, arg2: int) -> bool:
    """
    Brief description.
    
    Longer description explaining the purpose,
    behavior, and any important details.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When arg2 is negative
        
    Example:
        >>> my_function("hello", 42)
        True
    """
    pass
```

---

## Performance Considerations

When contributing code:

1. **Use Async Patterns**
   ```python
   # Good - non-blocking
   async def fetch_data():
       return await source.get_data()
   
   # Avoid - blocks event loop
   def fetch_data():
       return requests.get(url)
   ```

2. **Implement Caching**
   ```python
   # Cache expensive operations
   @cache(ttl=3600)
   async def expensive_operation(query):
       return await process(query)
   ```

3. **Batch Processing**
   ```python
   # Process multiple items together
   results = await asyncio.gather(*tasks)
   ```

---

## Adding New Data Sources

To add a new regulatory source:

### 1. Create Source Module

```python
# sources/new_source.py

async def get_latest_documents() -> List[Dict]:
    """Fetch latest documents from the source."""
    pass

async def fetch_document(doc_id: str) -> bytes:
    """Fetch a specific document."""
    pass
```

### 2. Register in Monitoring Agent

```python
# agents/monitoring_agent.py

# Add to sources dictionary
SOURCES = {
    "new_source": get_latest_documents,
    ...
}
```

### 3. Update Documentation

- Add to supported sources in README
- Update ARCHITECTURE.md with flow
- Add example queries

---

## Adding New Agents

To add a new agent:

### 1. Create Agent Class

```python
# agents/my_agent.py

from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    """Custom agent description."""
    
    async def process(self, data):
        """Process data and return results."""
        pass
```

### 2. Register in Graph

```python
# graph.py

my_agent = MyAgent()

async def my_agent_node(state: GraphState):
    """Node for my agent."""
    result = await my_agent.process(state)
    return {"key": result}

# In build_graph():
workflow.add_node("my_agent", my_agent_node)
workflow.add_edge("previous_node", "my_agent")
```

### 3. Add Tests

```python
# tests/test_my_agent.py

@pytest.mark.asyncio
async def test_my_agent():
    pass
```

---

## Debugging Tips

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Use Python Debugger

```python
import pdb

pdb.set_trace()  # Breakpoint
```

### Check State During Execution

```python
print(f"Current state: {state}")
print(f"Monitoring results: {state['monitoring_results']}")
```

---

## Review Process

### What We Look For

1. **Code Quality** ✓
   - Follows style guide
   - Well-documented
   - No code duplication

2. **Tests** ✓
   - Comprehensive coverage
   - Tests for edge cases
   - All tests pass

3. **Documentation** ✓
   - README updated
   - Docstrings complete
   - Examples provided

4. **Compatibility** ✓
   - Works with Python 3.8+
   - No breaking changes
   - Dependencies compatible

### Feedback & Iterations

- Reviewers may request changes
- Update your PR with requested changes
- Continue discussion in PR comments
- Once approved, merge!

---

## Common Issues & Solutions

### Issue: Merge Conflicts

```bash
git fetch origin
git rebase origin/main
# Resolve conflicts in files
git add .
git rebase --continue
git push --force-with-lease
```

### Issue: Large File Size

```bash
# Check file size
git ls-files -lS

# Use .gitignore for large files
echo "large_file.pkl" >> .gitignore
```

### Issue: Tests Failing

```bash
# Run tests locally
pytest tests/ -v

# Check test requirements
pip install -r requirements-dev.txt
```

---

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Acknowledged in releases
- Featured in monthly highlights

---

## Questions?

- 📧 Email: [project_email@example.com]
- 💬 GitHub Discussions: [Link]
- 🐦 Twitter: [@handle]

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙌**
