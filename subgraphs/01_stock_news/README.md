# Stock News Subgraph

This subgraph retrieves and processes stock market news from various sources.

## Components

### Nodes
1. **retrieve_stock_news** - Fetches news from RSS feeds (Yahoo Finance)
2. **filter_relevant_news** - Filters news by relevance score
3. **summarize_news** - Uses OpenAI to summarize relevant news

### Data Flow
```
START → retrieve_stock_news → filter_relevant_news → summarize_news → END
```

### Input
- `stock_symbols`: List of stock symbols to search news for

### Output
- `raw_news`: All retrieved news items
- `filtered_news`: News items with relevance score > 7
- `news_summary`: AI-generated summary of relevant news

### Data Sources
- Yahoo Finance RSS (Currently returns 404 - needs alternative)

### Dependencies
- OpenAI API for summarization
- feedparser for RSS parsing (or urllib/xml as fallback)