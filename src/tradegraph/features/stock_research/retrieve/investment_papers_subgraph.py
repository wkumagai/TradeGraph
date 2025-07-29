"""Investment Research Papers Retrieval Subgraph.

This subgraph retrieves recent academic papers and research on investment methods.
"""

from typing import Any, Dict, List
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.search_investment_papers import search_investment_papers_node
from .nodes.retrieve_paper_contents import retrieve_paper_contents_node
from .nodes.summarize_investment_papers import summarize_investment_papers_node
from .input_data import InvestmentMethodPapersState


class InvestmentPapersSubgraph(BaseSubgraph):
    """Subgraph for retrieving and processing investment research papers."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the InvestmentPapersSubgraph.
        
        Args:
            llm_name: Name of the LLM to use for processing
        """
        super().__init__(name="InvestmentPapersSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the investment papers retrieval graph."""
        workflow = StateGraph(InvestmentMethodPapersState)
        
        # Add nodes
        workflow.add_node("search_papers", search_investment_papers_node)
        workflow.add_node("retrieve_contents", retrieve_paper_contents_node)
        workflow.add_node("summarize_papers", summarize_investment_papers_node)
        
        # Define edges
        workflow.set_entry_point("search_papers")
        workflow.add_edge("search_papers", "retrieve_contents")
        workflow.add_edge("retrieve_contents", "summarize_papers")
        workflow.add_edge("summarize_papers", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the investment papers retrieval pipeline.
        
        Args:
            state: Initial state containing:
                - search_queries: List of search queries
                - time_range: Time range for papers (default: "1y")
                - paper_sources: List of sources (default: arxiv, ssrn)
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - paper_titles: List of paper titles and metadata
                - paper_contents: Full paper contents
                - paper_summaries: Summaries of papers
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        if "time_range" not in state:
            state["time_range"] = "1y"
        if "paper_sources" not in state:
            state["paper_sources"] = ["arxiv", "ssrn", "nber"]
        if "search_queries" not in state:
            state["search_queries"] = [
                "stock market anomalies machine learning",
                "algorithmic trading strategies",
                "portfolio optimization deep learning",
                "market prediction neural networks",
                "factor investing quantitative methods",
                "cryptocurrency trading strategies",
                "options pricing models ML"
            ]
        
        return graph.invoke(state)