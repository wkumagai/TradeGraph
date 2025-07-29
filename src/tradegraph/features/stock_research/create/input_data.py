"""Input data definitions for investment method creation subgraphs."""

from typing import List, Dict, Any, Optional, TypedDict


class InvestmentMethodState(TypedDict):
    """State for investment method creation."""
    # Inputs
    market_insights: str  # Insights from news analysis
    research_papers: str  # Summary of research papers
    investment_goals: List[str]  # Investment objectives
    constraints: List[str]  # Trading constraints
    llm_name: str
    save_dir: str
    
    # Generated outputs
    investment_idea: str  # Core investment thesis
    market_anomaly: Dict[str, Any]  # Identified market inefficiency
    trading_strategy: Dict[str, Any]  # Detailed trading rules
    investment_method: Dict[str, Any]  # Complete refined method
    

class AnomalyInferenceState(TypedDict):
    """State for anomaly inference."""
    market_data: Dict[str, Any]  # Historical market data
    patterns: List[Dict[str, Any]]  # Identified patterns
    anomalies: List[Dict[str, Any]]  # Detected anomalies
    statistical_tests: Dict[str, Any]  # Statistical validation
    llm_name: str
    save_dir: str