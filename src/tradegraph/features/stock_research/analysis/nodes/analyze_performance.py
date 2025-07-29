"""Node for analyzing backtest performance metrics."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def analyze_performance_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the performance metrics from backtest results.
    
    This node provides detailed analysis of strategy performance.
    """
    performance_metrics = state.get("performance_metrics", {})
    raw_results = state.get("raw_results", {})
    investment_method = state.get("investment_method", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Analyze these trading strategy backtest results in detail.

Performance Metrics:
{json.dumps(performance_metrics, indent=2)}

Investment Method:
{json.dumps(investment_method.get('method_name', 'Unknown'), indent=2)}
Expected Performance: {json.dumps(investment_method.get('performance_expectations', {}), indent=2)}

Provide comprehensive performance analysis:

{{
  "overall_assessment": {{
    "performance_grade": "A/B/C/D/F with explanation",
    "met_expectations": true/false,
    "key_strengths": ["List of strong points"],
    "key_weaknesses": ["List of weak points"]
  }},
  "return_analysis": {{
    "absolute_performance": {{
      "total_return": "X% with interpretation",
      "annualized_return": "X% vs Y% expected",
      "comparison_to_benchmark": "Outperformed/Underperformed by X%"
    }},
    "consistency": {{
      "monthly_consistency": "X% positive months",
      "volatility_assessment": "High/Medium/Low with X% annualized",
      "return_distribution": "Normal/Skewed/Fat-tailed"
    }}
  }},
  "risk_analysis": {{
    "drawdown_analysis": {{
      "max_drawdown": "X% - Acceptable/Concerning",
      "recovery_time": "X days - Fast/Average/Slow",
      "drawdown_frequency": "X times below -10%"
    }},
    "risk_metrics": {{
      "sharpe_ratio": "X - Excellent/Good/Poor",
      "sortino_ratio": "X - Better/Worse than Sharpe",
      "calmar_ratio": "X - Risk-reward assessment"
    }},
    "tail_risk": {{
      "var_95": "X% daily VaR",
      "worst_day": "X% loss on DATE",
      "black_swan_vulnerability": "High/Medium/Low"
    }}
  }},
  "trading_analysis": {{
    "efficiency": {{
      "win_rate": "X% - Interpretation",
      "profit_factor": "X - Good/Poor",
      "average_win_loss_ratio": "X:1"
    }},
    "execution": {{
      "number_of_trades": "X total (Y per month)",
      "holding_period": "Average X days",
      "turnover": "X% annually - High/Low"
    }},
    "costs": {{
      "transaction_costs": "X% of returns",
      "slippage_impact": "Estimated X% degradation",
      "net_vs_gross": "X% difference"
    }}
  }},
  "regime_performance": {{
    "bull_market": "X% return, Y Sharpe",
    "bear_market": "X% return, Y Sharpe",
    "high_volatility": "X% return, Y Sharpe",
    "performance_stability": "Consistent/Variable across regimes"
  }},
  "statistical_significance": {{
    "t_statistic": "X - Significant at Y% level",
    "information_ratio": "X - Skill assessment",
    "alpha": "X% - True alpha or luck?",
    "confidence_level": "X% confidence in results"
  }}
}}

Be specific with numbers and provide actionable interpretations."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        response = response.choices[0].message.content
        # Try to parse as JSON
        try:
            performance_analysis = json.loads(response)
        except json.JSONDecodeError:
            performance_analysis = {
                "analysis": response,
                "overall_assessment": {"performance_grade": "Pending"}
            }
    except Exception as e:
        print(f"Error analyzing performance: {e}")
        performance_analysis = {"error": str(e)}
    
    # Save performance analysis
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(os.path.join(save_dir, "analysis"), exist_ok=True)
    
    with open(os.path.join(save_dir, "analysis", "performance_analysis.json"), "w") as f:
        json.dump(performance_analysis, f, indent=2)
    
    # Update state
    state["performance_analysis"] = performance_analysis
    
    print("Performance analysis completed")
    
    return state