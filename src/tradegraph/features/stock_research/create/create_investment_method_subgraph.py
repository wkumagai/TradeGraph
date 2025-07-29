"""Create Investment Method Subgraph.

This subgraph generates novel investment strategies based on market analysis and research.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.generate_investment_idea import generate_investment_idea_node
from .nodes.design_trading_strategy import design_trading_strategy_node
from .nodes.identify_market_anomaly import identify_market_anomaly_node
from .nodes.refine_investment_method import refine_investment_method_node
from .input_data import InvestmentMethodState


class CreateInvestmentMethodSubgraph(BaseSubgraph):
    """Subgraph for creating novel investment methods and strategies."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the CreateInvestmentMethodSubgraph.
        
        Args:
            llm_name: Name of the LLM to use for generation
        """
        super().__init__(name="CreateInvestmentMethodSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the investment method creation graph."""
        workflow = StateGraph(InvestmentMethodState)
        
        # Add nodes
        workflow.add_node("generate_idea", generate_investment_idea_node)
        workflow.add_node("identify_anomaly", identify_market_anomaly_node)
        workflow.add_node("design_strategy", design_trading_strategy_node)
        workflow.add_node("refine_method", refine_investment_method_node)
        
        # Define flow
        workflow.set_entry_point("generate_idea")
        workflow.add_edge("generate_idea", "identify_anomaly")
        workflow.add_edge("identify_anomaly", "design_strategy")
        workflow.add_edge("design_strategy", "refine_method")
        workflow.add_edge("refine_method", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the investment method creation pipeline.
        
        Args:
            state: Initial state containing:
                - market_insights: Insights from news and research
                - research_papers: Summary of investment research
                - investment_goals: Specific goals (e.g., "high Sharpe", "low drawdown")
                - constraints: Any constraints (e.g., "long-only", "liquid assets")
                - llm_name: LLM to use
        
        Returns:
            Updated state with:
                - investment_idea: Core investment thesis
                - market_anomaly: Identified inefficiency to exploit
                - trading_strategy: Detailed trading rules
                - investment_method: Complete refined method
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        if "investment_goals" not in state:
            state["investment_goals"] = ["high Sharpe ratio", "consistent returns", "manageable risk"]
        if "constraints" not in state:
            state["constraints"] = ["liquid US equities", "no leverage", "daily rebalancing possible"]
        
        return graph.invoke(state)