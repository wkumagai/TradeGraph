"""Node for executing the backtest code."""

import os
import subprocess
import json
import time
from typing import Dict, Any


def execute_backtest_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the backtest code and capture results.
    
    This node runs the backtest script in a subprocess with timeout protection.
    """
    backtest_file = state.get("backtest_file", "")
    execution_dir = state.get("execution_dir", "")
    execution_params = state.get("execution_params", {})
    execution_logs = state.get("execution_logs", [])
    
    timeout = execution_params.get("timeout", 300)  # 5 minutes default
    
    try:
        execution_logs.append(f"Starting backtest execution with {timeout}s timeout...")
        
        # Validate execution directory
        if not execution_dir or not os.path.exists(execution_dir):
            raise ValueError(f"Invalid execution directory: {execution_dir}")
        
        # Change to execution directory
        original_dir = os.getcwd()
        os.chdir(execution_dir)
        
        # Run the backtest
        start_time = time.time()
        
        try:
            # Check if backtest file exists
            if not os.path.exists("backtest.py"):
                raise FileNotFoundError(f"Backtest file not found in {execution_dir}")
            
            # Try to use the virtual environment if it exists
            venv_python = os.path.join("venv", "bin", "python")
            if os.path.exists(venv_python):
                python_cmd = venv_python
            else:
                python_cmd = "python3"
            
            result = subprocess.run(
                [python_cmd, "backtest.py"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_time = time.time() - start_time
            
            execution_logs.append(f"Execution completed in {execution_time:.2f} seconds")
            execution_logs.append(f"Return code: {result.returncode}")
            
            # Capture output
            if result.stdout:
                execution_logs.append("=== STDOUT ===")
                execution_logs.append(result.stdout)
            
            if result.stderr:
                execution_logs.append("=== STDERR ===")
                execution_logs.append(result.stderr)
            
            # Check for success
            if result.returncode == 0:
                state["execution_status"] = "success"
                
                # Try to load results
                results_file = "backtest_results.json"
                if os.path.exists(results_file):
                    with open(results_file, "r") as f:
                        state["raw_results"] = json.load(f)
                    execution_logs.append("Successfully loaded backtest results")
                else:
                    execution_logs.append("Warning: No results file found")
                    state["raw_results"] = {"status": "completed", "output": result.stdout}
            else:
                state["execution_status"] = "failed"
                state["error_logs"] = [result.stderr] if result.stderr else ["Non-zero return code"]
                
        except subprocess.TimeoutExpired:
            execution_logs.append(f"Execution timed out after {timeout} seconds")
            state["execution_status"] = "failed"
            state["error_logs"] = ["Execution timeout"]
            
        except Exception as e:
            execution_logs.append(f"Execution error: {e}")
            state["execution_status"] = "failed"
            state["error_logs"] = [str(e)]
        
        finally:
            # Return to original directory
            os.chdir(original_dir)
        
        # Update state
        state["execution_logs"] = execution_logs
        
    except Exception as e:
        state["execution_logs"] = execution_logs + [f"Fatal error: {e}"]
        state["execution_status"] = "failed"
        state["error_logs"] = [str(e)]
    
    return state