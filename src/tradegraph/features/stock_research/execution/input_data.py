"""Input data definitions for execution subgraphs."""

from typing import List, Dict, Any, Optional, TypedDict


class ExperimentPlanState(TypedDict):
    """State for experiment planning."""
    # Inputs
    investment_method: Dict[str, Any]  # Complete investment method
    trading_strategy: Dict[str, Any]  # Trading strategy details
    test_period: str  # Time period for testing
    llm_name: str
    save_dir: str
    
    # Generated outputs
    experiment_design: Dict[str, Any]  # Overall experiment plan
    dataset_specification: Dict[str, Any]  # Data requirements
    evaluation_metrics: Dict[str, Any]  # Metrics to calculate
    backtest_code: str  # Executable Python code


class LocalExecutionState(TypedDict):
    """State for local experiment execution."""
    # Inputs
    backtest_code: str  # Code to execute
    dataset_specification: Dict[str, Any]  # Data requirements
    execution_params: Dict[str, Any]  # Execution parameters
    llm_name: str
    save_dir: str
    
    # Outputs
    execution_logs: List[str]  # Execution progress logs
    raw_results: Dict[str, Any]  # Raw backtest results
    performance_metrics: Dict[str, Any]  # Calculated metrics
    error_logs: List[str]  # Any errors encountered
    execution_status: str  # success/failed/partial


class ErrorCorrectionState(TypedDict):
    """State for error correction."""
    # Inputs
    original_code: str
    error_logs: List[str]
    execution_logs: List[str]
    llm_name: str
    
    # Outputs
    fixed_code: str
    fix_description: str
    retry_count: int