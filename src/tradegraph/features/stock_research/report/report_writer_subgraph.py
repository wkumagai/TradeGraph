"""Report Writer Subgraph for creating comprehensive investment research reports.

This subgraph generates professional reports from all research phases.
"""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from ....core.base import BaseSubgraph
from .nodes.compile_sections import compile_sections_node
from .nodes.write_report import write_report_node
from .nodes.create_visualizations import create_visualizations_node
from .nodes.generate_html import generate_html_node
from .input_data import ReportState


class ReportWriterSubgraph(BaseSubgraph):
    """Subgraph for writing investment research reports."""
    
    def __init__(self, llm_name: str = "gpt-4o-mini-2024-07-18"):
        """Initialize the ReportWriterSubgraph.
        
        Args:
            llm_name: Name of the LLM to use
        """
        super().__init__(name="ReportWriterSubgraph")
        self.llm_name = llm_name
    
    def build_graph(self):
        """Build the report writing graph."""
        workflow = StateGraph(ReportState)
        
        # Add nodes
        workflow.add_node("compile_sections", compile_sections_node)
        workflow.add_node("create_visualizations", create_visualizations_node)
        workflow.add_node("write_report", write_report_node)
        workflow.add_node("generate_html", generate_html_node)
        
        # Define flow
        workflow.set_entry_point("compile_sections")
        workflow.add_edge("compile_sections", "create_visualizations")
        workflow.add_edge("create_visualizations", "write_report")
        workflow.add_edge("write_report", "generate_html")
        workflow.add_edge("generate_html", END)
        
        return workflow.compile()
    
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the report writing pipeline.
        
        Args:
            state: State containing all research outputs
        
        Returns:
            Updated state with:
                - report_sections: Organized content
                - visualizations: Generated charts
                - final_report: Complete markdown report
                - html_report: HTML version
        """
        graph = self.build_graph()
        
        # Set defaults
        if "llm_name" not in state:
            state["llm_name"] = self.llm_name
        
        return graph.invoke(state)