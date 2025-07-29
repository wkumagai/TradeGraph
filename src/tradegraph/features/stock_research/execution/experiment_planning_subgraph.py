"""Experiment Planning Subgraph for Stock Trading Strategies.

This subgraph creates comprehensive experiment plans for testing investment methods.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.design_experiment import design_experiment_node
from .nodes.prepare_datasets import prepare_datasets_node
from .nodes.define_metrics import define_metrics_node
from .nodes.create_backtest_code import create_backtest_code_node
from .input_data import ExperimentPlanState


class ExperimentPlanningSubgraph(BaseSubgraph):
    """Subgraph for planning trading strategy experiments."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the ExperimentPlanningSubgraph.
        
        Args:
            llm_name: Name of the LLM to use
        """
        super().__init__(name="ExperimentPlanningSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the experiment planning graph."""
        workflow = StateGraph(ExperimentPlanState)
        
        # Add nodes
        workflow.add_node("design_experiment", design_experiment_node)
        workflow.add_node("prepare_datasets", prepare_datasets_node)
        workflow.add_node("define_metrics", define_metrics_node)
        workflow.add_node("create_backtest_code", create_backtest_code_node)
        
        # Define flow
        workflow.set_entry_point("design_experiment")
        workflow.add_edge("design_experiment", "prepare_datasets")
        workflow.add_edge("prepare_datasets", "define_metrics")
        workflow.add_edge("define_metrics", "create_backtest_code")
        workflow.add_edge("create_backtest_code", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the experiment planning pipeline.
        
        Args:
            state: Initial state containing:
                - investment_method: Complete investment method details
                - trading_strategy: Trading strategy specification
                - test_period: Time period for backtesting
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - experiment_design: Overall experiment plan
                - dataset_specification: Data requirements and sources
                - evaluation_metrics: Performance metrics to calculate
                - backtest_code: Executable backtesting code
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        if "test_period" not in state:
            state["test_period"] = "2019-2024"  # 5 years default
        
        return graph.invoke(state)