"""Stock News Retrieval Subgraph.

This subgraph retrieves recent stock market news, particularly focusing on US stocks.
"""

from typing import Any, Dict, List
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from ....core.base import BaseSubgraph
from .nodes.retrieve_stock_news import retrieve_stock_news_node
from .nodes.filter_relevant_news import filter_relevant_news_node
from .nodes.summarize_news import summarize_news_node
from .input_data import StockNewsState


class StockNewsSubgraph(BaseSubgraph):
    """Subgraph for retrieving and processing stock market news."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the StockNewsSubgraph.
        
        Args:
            llm_name: Name of the LLM to use for processing
        """
        super().__init__(name="StockNewsSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the stock news retrieval graph."""
        workflow = StateGraph(StockNewsState)
        
        # Add nodes
        workflow.add_node("retrieve_news", retrieve_stock_news_node)
        workflow.add_node("filter_news", filter_relevant_news_node)
        workflow.add_node("summarize_news", summarize_news_node)
        
        # Define edges
        workflow.set_entry_point("retrieve_news")
        workflow.add_edge("retrieve_news", "filter_news")
        workflow.add_edge("filter_news", "summarize_news")
        workflow.add_edge("summarize_news", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the stock news retrieval pipeline.
        
        Args:
            state: Initial state containing:
                - stock_symbols: List of stock symbols to focus on
                - time_period: Time period for news (e.g., "24h", "7d")
                - news_sources: List of news sources to use
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - raw_news: List of retrieved news articles
                - filtered_news: List of relevant news
                - news_summary: Summary of important news
        """
        graph = self.build_graph()
        
        # Set default values
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        if "time_period" not in state:
            state["time_period"] = "24h"
        if "news_sources" not in state:
            state["news_sources"] = ["reuters", "bloomberg", "wsj", "cnbc"]
        
        return graph.invoke(state)