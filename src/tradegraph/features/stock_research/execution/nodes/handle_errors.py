"""Node for handling execution errors."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def handle_errors_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Handle errors that occurred during backtest execution.
    
    This node analyzes errors and suggests fixes.
    """
    error_logs = state.get("error_logs", [])
    execution_logs = state.get("execution_logs", [])
    backtest_code = state.get("backtest_code", "")
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    # Combine all error information
    error_context = {
        "error_logs": error_logs,
        "execution_logs": execution_logs[-20:],  # Last 20 log entries
        "code_snippet": backtest_code[:1000] if len(backtest_code) > 1000 else backtest_code
    }
    
    prompt = f"""Analyze these backtest execution errors and suggest fixes.

Error Context:
{json.dumps(error_context, indent=2)}

Provide:
1. Error diagnosis - what went wrong
2. Root cause - why it failed
3. Suggested fixes - how to fix it
4. Common issues - if this is a known problem

Focus on practical, actionable solutions."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        error_analysis = content
        
        # Save error analysis
        save_dir = state.get("save_dir", "./stock_research_output")
        error_report = {
            "errors": error_logs,
            "analysis": error_analysis,
            "execution_logs": execution_logs,
            "status": "failed"
        }
        
        with open(os.path.join(save_dir, "execution", "error_report.json"), "w") as f:
            json.dump(error_report, f, indent=2)
        
        # Update state with minimal metrics
        state["performance_metrics"] = {
            "execution_status": "failed",
            "error_count": len(error_logs),
            "error_summary": error_analysis[:200]
        }
        
    except Exception as e:
        state["performance_metrics"] = {
            "execution_status": "failed",
            "error_count": len(error_logs),
            "analysis_error": str(e)
        }
    
    return state