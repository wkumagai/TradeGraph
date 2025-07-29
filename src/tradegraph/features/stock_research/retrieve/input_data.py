"""Input data definitions for stock research retrieval subgraphs."""

from typing import List, Dict, Any, Optional, TypedDict


class StockNewsState(TypedDict):
    """State for stock news retrieval."""
    stock_symbols: List[str]  # Stock symbols to focus on
    time_period: str  # Time period for news (e.g., "24h", "7d", "30d")
    news_sources: List[str]  # News sources to use
    llm_name: str  # LLM to use for processing
    raw_news: List[Dict[str, Any]]  # Retrieved news articles
    filtered_news: List[Dict[str, Any]]  # Relevant news after filtering
    news_summary: str  # Summary of important news
    save_dir: str  # Directory to save results


class InvestmentMethodPapersState(TypedDict):
    """State for investment method papers retrieval."""
    search_queries: List[str]  # Search queries for papers
    time_range: str  # Time range for papers (e.g., "1y", "6m")
    paper_sources: List[str]  # Sources like arxiv, ssrn, etc.
    llm_name: str
    paper_titles: List[Dict[str, str]]  # Retrieved paper titles and metadata
    paper_contents: List[Dict[str, Any]]  # Full paper contents
    paper_summaries: List[Dict[str, str]]  # Summaries of papers
    save_dir: str


class MarketDataState(TypedDict):
    """State for market data retrieval."""
    stock_symbols: List[str]  # Stock symbols to retrieve data for
    data_types: List[str]  # Types of data (price, volume, fundamentals, etc.)
    time_period: str  # Historical period
    data_frequency: str  # Data frequency (daily, hourly, etc.)
    market_data: Dict[str, Any]  # Retrieved market data
    data_summary: str  # Summary of market conditions
    save_dir: str