"""Stock research retrieval subgraphs."""

from .stock_news_subgraph import StockNewsSubgraph
from .investment_papers_subgraph import InvestmentPapersSubgraph

__all__ = [
    "StockNewsSubgraph",
    "InvestmentPapersSubgraph"
]