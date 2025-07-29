"""Input data definitions for report generation subgraphs."""

from typing import List, Dict, Any, Optional, TypedDict


class ReportState(TypedDict):
    """State for report generation."""
    # All inputs from previous phases
    news_summary: str
    paper_summaries: List[Dict[str, Any]]
    investment_method: Dict[str, Any]
    market_anomaly: Dict[str, Any]
    trading_strategy: Dict[str, Any]
    experiment_design: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    strategy_evaluation: Dict[str, Any]
    key_insights: List[str]
    improvement_suggestions: List[Dict[str, Any]]
    
    # Report generation
    llm_name: str
    save_dir: str
    
    # Generated outputs
    report_sections: Dict[str, str]  # Organized sections
    visualizations: List[Dict[str, Any]]  # Charts and graphs
    final_report: str  # Complete markdown report
    html_report: str  # HTML version