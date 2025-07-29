"""Stock research subgraphs for AIRAS-Trade."""

# Research and Information Gathering
from .retrieve import StockNewsSubgraph, InvestmentPapersSubgraph

# Investment Method Creation
from .create import CreateInvestmentMethodSubgraph

# Experiment Planning and Execution
from .execution import ExperimentPlanningSubgraph, LocalExecutionSubgraph

# Analysis and Evaluation
from .analysis import ResultsAnalysisSubgraph

# Report Generation
from .report import ReportWriterSubgraph

__all__ = [
    # Retrieve
    "StockNewsSubgraph",
    "InvestmentPapersSubgraph",
    # Create
    "CreateInvestmentMethodSubgraph",
    # Execution
    "ExperimentPlanningSubgraph",
    "LocalExecutionSubgraph",
    # Analysis
    "ResultsAnalysisSubgraph",
    # Report
    "ReportWriterSubgraph"
]