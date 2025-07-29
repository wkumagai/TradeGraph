# Investment Papers Subgraph

This subgraph searches for and retrieves academic papers related to quantitative finance and algorithmic trading.

## Components

### Nodes
1. **search_papers** - Searches ArXiv API for relevant papers
2. **filter_papers** - Filters papers by finance-related keywords
3. **extract_methods** - Extracts trading strategies and methods

### Data Flow
```
START → search_papers → filter_papers → extract_methods → END
```

### Input
- Search queries (predefined):
  - "machine learning trading strategy"
  - "portfolio optimization"
  - "quantitative finance"

### Output
- `papers`: List of relevant academic papers with:
  - Title
  - Authors
  - Abstract
  - ArXiv ID
  - Publication date
  - Extracted methods

### Data Sources
- ArXiv API (export.arxiv.org) - ✅ Working

### Example Output
Typically retrieves 6-10 papers on algorithmic trading, portfolio optimization, and quantitative methods.