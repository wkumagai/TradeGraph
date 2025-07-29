"""Node for setting up the execution environment."""

import os
import subprocess
import tempfile
from typing import Dict, Any


def setup_environment_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Set up the local environment for backtest execution.
    
    This node prepares a clean environment with necessary dependencies.
    """
    backtest_code = state.get("backtest_code", "")
    save_dir = state.get("save_dir", "./stock_research_output")
    
    execution_logs = []
    
    try:
        # Create execution directory
        exec_dir = os.path.join(save_dir, "execution")
        os.makedirs(exec_dir, exist_ok=True)
        
        # Save the backtest code
        backtest_file = os.path.join(exec_dir, "backtest.py")
        with open(backtest_file, "w") as f:
            f.write(backtest_code)
        execution_logs.append(f"Saved backtest code to {backtest_file}")
        
        # Create requirements file if not exists
        requirements_file = os.path.join(exec_dir, "requirements.txt")
        if not os.path.exists(requirements_file):
            requirements = """numpy>=1.21.0
pandas>=1.3.0
yfinance>=0.2.18
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
scikit-learn>=1.0.0
ta>=0.10.2
quantstats>=0.0.59
"""
            with open(requirements_file, "w") as f:
                f.write(requirements)
        
        # Check if we can create a virtual environment
        try:
            venv_dir = os.path.join(exec_dir, "venv")
            if not os.path.exists(venv_dir):
                subprocess.run(
                    ["python3", "-m", "venv", venv_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
                execution_logs.append(f"Created virtual environment at {venv_dir}")
        except Exception as e:
            execution_logs.append(f"Warning: Could not create venv: {e}")
        
        # Update state
        state["execution_logs"] = execution_logs
        state["execution_dir"] = exec_dir
        state["backtest_file"] = backtest_file
        
    except Exception as e:
        state["execution_logs"] = execution_logs + [f"Error in setup: {e}"]
        state["execution_status"] = "failed"
        state["error_logs"] = [str(e)]
    
    return state