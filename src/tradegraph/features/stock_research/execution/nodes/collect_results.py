"""Node for collecting and processing backtest results."""

import os
import json
import glob
from typing import Dict, Any


def collect_results_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Collect and process the backtest results.
    
    This node gathers all output files and extracts performance metrics.
    """
    execution_dir = state.get("execution_dir", "")
    raw_results = state.get("raw_results", {})
    execution_logs = state.get("execution_logs", [])
    
    try:
        execution_logs.append("Collecting backtest results...")
        
        # Initialize performance metrics
        performance_metrics = {}
        
        # Extract metrics from raw results
        if isinstance(raw_results, dict):
            # Standard metrics
            metrics_keys = [
                "total_return", "cagr", "volatility", "sharpe_ratio",
                "max_drawdown", "win_rate", "profit_factor",
                "number_of_trades", "alpha", "beta"
            ]
            
            for key in metrics_keys:
                if key in raw_results:
                    performance_metrics[key] = raw_results[key]
            
            # Extract nested metrics
            if "return_metrics" in raw_results:
                performance_metrics.update(raw_results["return_metrics"])
            if "risk_metrics" in raw_results:
                performance_metrics.update(raw_results["risk_metrics"])
            if "trading_metrics" in raw_results:
                performance_metrics.update(raw_results["trading_metrics"])
        
        # Look for additional output files
        result_files = []
        
        # Check for plots
        plot_patterns = ["*.png", "*.jpg", "*.pdf"]
        for pattern in plot_patterns:
            plots = glob.glob(os.path.join(execution_dir, pattern))
            for plot in plots:
                result_files.append({
                    "type": "plot",
                    "file": os.path.basename(plot),
                    "path": plot
                })
                execution_logs.append(f"Found plot: {os.path.basename(plot)}")
        
        # Check for CSV results
        csv_files = glob.glob(os.path.join(execution_dir, "*.csv"))
        for csv_file in csv_files:
            result_files.append({
                "type": "data",
                "file": os.path.basename(csv_file),
                "path": csv_file
            })
            execution_logs.append(f"Found data file: {os.path.basename(csv_file)}")
        
        # Check for log files
        log_files = glob.glob(os.path.join(execution_dir, "*.log"))
        for log_file in log_files:
            result_files.append({
                "type": "log",
                "file": os.path.basename(log_file),
                "path": log_file
            })
        
        # Create summary
        summary = {
            "execution_status": "success",
            "metrics_count": len(performance_metrics),
            "files_generated": len(result_files),
            "key_metrics": {
                "total_return": performance_metrics.get("total_return", "N/A"),
                "sharpe_ratio": performance_metrics.get("sharpe_ratio", "N/A"),
                "max_drawdown": performance_metrics.get("max_drawdown", "N/A"),
                "win_rate": performance_metrics.get("win_rate", "N/A")
            }
        }
        
        # Save collected results
        results_summary = {
            "summary": summary,
            "performance_metrics": performance_metrics,
            "raw_results": raw_results,
            "output_files": result_files
        }
        
        summary_file = os.path.join(execution_dir, "results_summary.json")
        with open(summary_file, "w") as f:
            json.dump(results_summary, f, indent=2)
        
        execution_logs.append(f"Results summary saved to {summary_file}")
        execution_logs.append(f"Collected {len(performance_metrics)} metrics and {len(result_files)} output files")
        
        # Update state
        state["performance_metrics"] = performance_metrics
        state["execution_logs"] = execution_logs
        state["result_files"] = result_files
        
    except Exception as e:
        state["execution_logs"] = execution_logs + [f"Error collecting results: {e}"]
        state["error_logs"] = state.get("error_logs", []) + [str(e)]
    
    return state