"""Node for designing trading strategy experiments."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def design_experiment_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Design a comprehensive experiment plan for testing the trading strategy.
    
    This node creates a detailed experimental framework including test periods,
    validation approaches, and robustness checks.
    """
    investment_method = state.get("investment_method", {})
    trading_strategy = state.get("trading_strategy", {})
    test_period = state.get("test_period", "2019-2024")
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Design a comprehensive experiment plan for testing this trading strategy.

Investment Method:
{json.dumps(investment_method, indent=2)}

Trading Strategy:
{json.dumps(trading_strategy, indent=2)}

Test Period: {test_period}

Create a detailed experiment design with:

{{
  "experiment_name": "Descriptive name",
  "objectives": [
    "Primary: Validate strategy performance",
    "Secondary: Test robustness across market conditions",
    "Tertiary: Identify optimal parameters"
  ],
  "methodology": {{
    "backtest_approach": {{
      "type": "walk_forward/expanding_window/rolling_window",
      "train_period": "Length of training window",
      "test_period": "Length of test window",
      "step_size": "How often to retrain"
    }},
    "data_split": {{
      "in_sample": "{{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}}",
      "out_of_sample": "{{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}}",
      "validation": "Hold-out period for final validation"
    }},
    "parameter_optimization": {{
      "method": "grid_search/random_search/bayesian_optimization",
      "parameters_to_optimize": [
        {{"name": "param1", "range": [min, max], "step": step_size}}
      ],
      "objective_function": "Sharpe ratio/Total return/Calmar ratio"
    }}
  }},
  "robustness_tests": [
    {{
      "test_name": "Transaction cost sensitivity",
      "description": "Test with varying transaction costs",
      "parameters": {{"cost_range": [0.001, 0.01], "step": 0.001}}
    }},
    {{
      "test_name": "Market regime analysis", 
      "description": "Performance across bull/bear/sideways markets",
      "regime_detection": "Method to identify regimes"
    }},
    {{
      "test_name": "Parameter stability",
      "description": "How sensitive is performance to parameters",
      "method": "Monte Carlo parameter perturbation"
    }}
  ],
  "statistical_validation": {{
    "significance_tests": [
      "t-test for returns vs benchmark",
      "Sharpe ratio difference test",
      "Maximum drawdown distribution"
    ],
    "bootstrap_confidence": {{
      "n_simulations": 1000,
      "confidence_level": 0.95
    }}
  }},
  "benchmark_comparison": {{
    "benchmarks": [
      "S&P 500 (SPY)",
      "60/40 Portfolio",
      "Risk Parity",
      "Buy and Hold top stocks"
    ],
    "comparison_metrics": [
      "Risk-adjusted returns",
      "Drawdown characteristics",
      "Correlation analysis"
    ]
  }},
  "implementation_tests": {{
    "execution_feasibility": {{
      "test": "Can trades be executed at assumed prices",
      "slippage_model": "Conservative slippage assumptions"
    }},
    "capacity_analysis": {{
      "test": "Maximum capital before strategy degrades",
      "method": "Market impact modeling"
    }}
  }},
  "experiment_phases": [
    {{
      "phase": 1,
      "name": "Initial validation",
      "duration": "1 week",
      "goals": ["Confirm code works", "Get baseline results"]
    }},
    {{
      "phase": 2,
      "name": "Parameter optimization",
      "duration": "1 week", 
      "goals": ["Find optimal parameters", "Test stability"]
    }},
    {{
      "phase": 3,
      "name": "Robustness testing",
      "duration": "1 week",
      "goals": ["Stress test strategy", "Identify failure modes"]
    }}
  ]
}}

Design an experiment that will thoroughly validate the strategy and identify any weaknesses."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        response = content
        # Try to parse as JSON
        try:
            experiment_design = json.loads(response)
        except json.JSONDecodeError:
            experiment_design = {
                "experiment_name": "Trading Strategy Test",
                "description": response,
                "methodology": {"approach": "Standard backtest"}
            }
    except Exception as e:
        print(f"Error designing experiment: {e}")
        experiment_design = {
            "experiment_name": "Error",
            "error": str(e)
        }
    
    # Save experiment design
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(os.path.join(save_dir, "experiment"), exist_ok=True)
    
    with open(os.path.join(save_dir, "experiment", "experiment_design.json"), "w") as f:
        json.dump(experiment_design, f, indent=2)
    
    # Update state
    state["experiment_design"] = experiment_design
    
    print("Experiment design completed")
    
    return state