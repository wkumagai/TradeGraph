"""Input data definitions for analysis subgraphs."""

from typing import List, Dict, Any, Optional, TypedDict


class AnalysisState(TypedDict):
    """State for results analysis."""
    # Inputs
    performance_metrics: Dict[str, Any]  # Calculated metrics
    raw_results: Dict[str, Any]  # Raw backtest output
    investment_method: Dict[str, Any]  # Original method
    experiment_design: Dict[str, Any]  # Experiment parameters
    llm_name: str
    save_dir: str
    
    # Generated outputs
    performance_analysis: Dict[str, Any]  # Performance breakdown
    strategy_evaluation: Dict[str, Any]  # Strategy assessment
    key_insights: List[str]  # Main findings
    improvement_suggestions: List[Dict[str, Any]]  # Recommendations