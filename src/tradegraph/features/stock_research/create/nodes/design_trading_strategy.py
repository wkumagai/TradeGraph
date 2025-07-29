"""Node for designing detailed trading strategy."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def design_trading_strategy_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Design a comprehensive trading strategy to exploit the identified anomaly.
    
    This node creates detailed, implementable trading rules based on
    the investment idea and identified market anomaly.
    """
    investment_idea = state.get("investment_idea", "")
    market_anomaly = state.get("market_anomaly", {})
    investment_goals = state.get("investment_goals", [])
    constraints = state.get("constraints", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Design a comprehensive trading strategy to exploit the identified market anomaly.

Investment Idea:
{investment_idea}

Market Anomaly:
{json.dumps(market_anomaly, indent=2)}

Investment Goals:
{json.dumps(investment_goals, indent=2)}

Constraints:
{json.dumps(constraints, indent=2)}

Create a detailed trading strategy with the following JSON structure:

{{
  "strategy_name": "Descriptive strategy name",
  "strategy_type": "momentum/mean_reversion/arbitrage/factor/event_driven/ml_based",
  "universe": {{
    "asset_classes": ["equities/bonds/commodities/crypto"],
    "specific_criteria": "Market cap > $1B, volume > 1M shares/day, etc.",
    "number_of_assets": "Typical portfolio size",
    "rebalancing_frequency": "daily/weekly/monthly"
  }},
  "signal_generation": {{
    "primary_indicators": [
      {{
        "name": "Indicator name",
        "calculation": "Exact formula",
        "parameters": {{}},
        "data_requirements": []
      }}
    ],
    "signal_combination": "How multiple signals are combined",
    "signal_strength": "How to measure signal confidence"
  }},
  "entry_rules": {{
    "conditions": ["Specific conditions that must be met"],
    "timing": "Market open/close/intraday",
    "order_types": "Market/limit/stop",
    "position_sizing": {{
      "method": "Equal weight/volatility parity/Kelly criterion",
      "formula": "Exact calculation",
      "constraints": "Max position size, etc."
    }}
  }},
  "exit_rules": {{
    "profit_targets": "Specific levels or conditions",
    "stop_losses": "Fixed percentage/ATR-based/time-based",
    "time_exits": "Maximum holding period",
    "signal_reversal": "Exit on opposite signal?"
  }},
  "risk_management": {{
    "portfolio_level": {{
      "max_leverage": "1.0 for long-only",
      "max_concentration": "Max % in single position",
      "sector_limits": "Diversification requirements",
      "correlation_limits": "Max portfolio correlation"
    }},
    "position_level": {{
      "position_limits": "Max size per position",
      "stop_loss": "Percentage or volatility-based",
      "trailing_stops": "Implementation details"
    }},
    "drawdown_control": {{
      "max_drawdown": "Acceptable maximum",
      "drawdown_action": "Reduce size/stop trading"
    }}
  }},
  "implementation": {{
    "execution_algo": "VWAP/TWAP/Aggressive/Passive",
    "slippage_model": "Expected transaction costs",
    "data_pipeline": {{
      "sources": ["Required data sources"],
      "frequency": "Real-time/daily/minute",
      "preprocessing": "Cleaning and normalization steps"
    }},
    "computational_requirements": "Processing power needed"
  }},
  "backtesting_plan": {{
    "historical_period": "Recommended test period",
    "out_of_sample": "Walk-forward approach",
    "performance_metrics": ["Sharpe", "Sortino", "Max DD", "Win rate"],
    "robustness_tests": ["Parameter sensitivity", "Regime analysis"]
  }},
  "expected_performance": {{
    "return": "Annual expected return",
    "volatility": "Expected volatility",
    "sharpe_ratio": "Risk-adjusted return",
    "max_drawdown": "Expected worst case",
    "correlation": "To S&P 500 or other benchmarks"
  }}
}}

Design a strategy that is:
1. Concrete and implementable
2. Robust to market regime changes
3. Scalable within constraints
4. Cost-effective after transaction costs

Provide specific formulas and parameters."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500,
            response_format={"type": "json_object"}
        )
        response_text = response.choices[0].message.content
        # Try to parse as JSON
        try:
            trading_strategy = json.loads(response_text)
        except json.JSONDecodeError:
            # Create basic structure if JSON parsing fails
            trading_strategy = {
                "strategy_name": "Generated Strategy",
                "description": response_text,
                "implementation": {"status": "To be refined"}
            }
    except Exception as e:
        print(f"Error designing strategy: {e}")
        trading_strategy = {
            "strategy_name": "Error",
            "description": "Failed to design strategy",
            "error": str(e)
        }
    
    # Save the trading strategy
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "investment_method", "trading_strategy.json"), "w") as f:
        json.dump(trading_strategy, f, indent=2)
    
    # Update state
    state["trading_strategy"] = trading_strategy
    
    print(f"Designed trading strategy: {trading_strategy.get('strategy_name', 'Unknown')}")
    
    return state