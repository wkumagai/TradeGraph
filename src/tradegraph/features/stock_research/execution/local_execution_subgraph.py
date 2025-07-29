"""Local Execution Subgraph for running backtests locally.

This subgraph executes the generated backtest code locally instead of on GitHub Actions.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.setup_environment import setup_environment_node
from .nodes.execute_backtest import execute_backtest_node
from .nodes.collect_results import collect_results_node
from .nodes.handle_errors import handle_errors_node
from .input_data import LocalExecutionState


class LocalExecutionSubgraph(BaseSubgraph):
    """Subgraph for executing trading strategy backtests locally."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the LocalExecutionSubgraph.
        
        Args:
            llm_name: Name of the LLM to use
        """
        super().__init__(name="LocalExecutionSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the local execution graph."""
        workflow = StateGraph(LocalExecutionState)
        
        # Add nodes
        workflow.add_node("setup_environment", setup_environment_node)
        workflow.add_node("execute_backtest", execute_backtest_node)
        workflow.add_node("collect_results", collect_results_node)
        workflow.add_node("handle_errors", handle_errors_node)
        
        # Define flow with conditional edges
        workflow.set_entry_point("setup_environment")
        workflow.add_edge("setup_environment", "execute_backtest")
        
        # Conditional edge based on execution success
        workflow.add_conditional_edges(
            "execute_backtest",
            self._check_execution_status,
            {
                "success": "collect_results",
                "failed": "handle_errors"
            }
        )
        
        workflow.add_edge("collect_results", END)
        workflow.add_edge("handle_errors", END)
        
        return workflow.compile()
    
    def _check_execution_status(self, state: Dict[str, Any]) -> str:
        """Check if execution was successful."""
        return state.get("execution_status", "failed")
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the local execution pipeline.
        
        Args:
            state: Initial state containing:
                - backtest_code: Code to execute
                - dataset_specification: Data requirements
                - execution_params: Execution parameters
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - execution_logs: Execution progress
                - raw_results: Backtest results
                - performance_metrics: Calculated metrics
                - execution_status: success/failed
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        if "execution_params" not in state:
            state["execution_params"] = {
                "timeout": 300,  # 5 minutes
                "memory_limit": "2GB"
            }
        
        return graph.invoke(state)