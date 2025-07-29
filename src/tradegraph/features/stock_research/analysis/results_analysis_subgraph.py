"""Results Analysis Subgraph for evaluating backtest performance.

This subgraph analyzes experiment results and generates insights.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.analyze_performance import analyze_performance_node
from .nodes.evaluate_strategy import evaluate_strategy_node
from .nodes.generate_insights import generate_insights_node
from .nodes.review_results import review_results_node
from .input_data import AnalysisState


class ResultsAnalysisSubgraph(BaseSubgraph):
    """Subgraph for analyzing trading strategy results."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the ResultsAnalysisSubgraph.
        
        Args:
            llm_name: Name of the LLM to use
        """
        super().__init__(name="ResultsAnalysisSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the results analysis graph."""
        workflow = StateGraph(AnalysisState)
        
        # Add nodes
        workflow.add_node("analyze_performance", analyze_performance_node)
        workflow.add_node("evaluate_strategy", evaluate_strategy_node)
        workflow.add_node("generate_insights", generate_insights_node)
        workflow.add_node("review_results", review_results_node)
        
        # Define flow
        workflow.set_entry_point("analyze_performance")
        workflow.add_edge("analyze_performance", "evaluate_strategy")
        workflow.add_edge("evaluate_strategy", "generate_insights")
        workflow.add_edge("generate_insights", "review_results")
        workflow.add_edge("review_results", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the results analysis pipeline.
        
        Args:
            state: Initial state containing:
                - performance_metrics: Backtest performance metrics
                - raw_results: Raw backtest output
                - investment_method: Original investment method
                - experiment_design: Experiment parameters
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - performance_analysis: Detailed performance breakdown
                - strategy_evaluation: Strategy effectiveness assessment
                - key_insights: Actionable insights
                - improvement_suggestions: Recommendations
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        
        return graph.invoke(state)