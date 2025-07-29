"""Node for defining evaluation metrics."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def define_metrics_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Define comprehensive evaluation metrics for the trading strategy.
    
    This node specifies all performance metrics to calculate during backtesting.
    """
    trading_strategy = state.get("trading_strategy", {})
    investment_goals = state.get("investment_goals", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Define comprehensive evaluation metrics for this trading strategy.

Trading Strategy:
{json.dumps(trading_strategy, indent=2)}

Investment Goals:
{json.dumps(investment_goals, indent=2)}

Create detailed metric specifications:

{{
  "return_metrics": {{
    "total_return": {{
      "formula": "(final_value - initial_value) / initial_value",
      "annualized": true,
      "description": "Total portfolio return"
    }},
    "cagr": {{
      "formula": "(final_value / initial_value) ^ (1 / years) - 1",
      "description": "Compound annual growth rate"
    }},
    "monthly_returns": {{
      "calculation": "Aggregate daily returns by month",
      "statistics": ["mean", "std", "skew", "kurtosis"]
    }}
  }},
  "risk_metrics": {{
    "volatility": {{
      "formula": "returns.std() * sqrt(252)",
      "description": "Annualized volatility"
    }},
    "max_drawdown": {{
      "formula": "(trough - peak) / peak",
      "description": "Maximum peak to trough decline"
    }},
    "drawdown_duration": {{
      "calculation": "Days from peak to recovery",
      "description": "Longest drawdown period"
    }},
    "var_95": {{
      "formula": "returns.quantile(0.05)",
      "description": "95% Value at Risk"
    }},
    "cvar_95": {{
      "formula": "returns[returns <= var_95].mean()",
      "description": "95% Conditional Value at Risk"
    }}
  }},
  "risk_adjusted_metrics": {{
    "sharpe_ratio": {{
      "formula": "(returns.mean() - rf_rate) / returns.std() * sqrt(252)",
      "rf_rate": 0.02,
      "description": "Risk-adjusted return"
    }},
    "sortino_ratio": {{
      "formula": "(returns.mean() - rf_rate) / downside_deviation * sqrt(252)",
      "description": "Downside risk-adjusted return"
    }},
    "calmar_ratio": {{
      "formula": "cagr / abs(max_drawdown)",
      "description": "Return over max drawdown"
    }},
    "information_ratio": {{
      "formula": "(returns - benchmark_returns).mean() / tracking_error * sqrt(252)",
      "description": "Active return over active risk"
    }}
  }},
  "trading_metrics": {{
    "number_of_trades": {{
      "calculation": "Count of all executed trades",
      "breakdown": ["longs", "shorts", "by_symbol"]
    }},
    "win_rate": {{
      "formula": "winning_trades / total_trades",
      "description": "Percentage of profitable trades"
    }},
    "profit_factor": {{
      "formula": "gross_profits / gross_losses",
      "description": "Ratio of wins to losses"
    }},
    "average_win_loss": {{
      "avg_win": "Average profit on winning trades",
      "avg_loss": "Average loss on losing trades",
      "ratio": "avg_win / abs(avg_loss)"
    }},
    "holding_period": {{
      "average": "Mean days positions are held",
      "median": "Median holding period",
      "distribution": "Histogram of holding periods"
    }}
  }},
  "portfolio_metrics": {{
    "turnover": {{
      "formula": "sum(abs(trades)) / avg_portfolio_value",
      "annualized": true,
      "description": "Portfolio turnover rate"
    }},
    "concentration": {{
      "herfindahl": "Sum of squared position weights",
      "top_5_weight": "Weight of 5 largest positions",
      "effective_n": "1 / herfindahl"
    }},
    "sector_exposure": {{
      "calculation": "Average weight by sector",
      "limits_breached": "Count of sector limit violations"
    }}
  }},
  "cost_metrics": {{
    "transaction_costs": {{
      "total": "Sum of all transaction costs",
      "per_trade": "Average cost per trade",
      "as_pct_returns": "Costs / gross_returns"
    }},
    "slippage": {{
      "estimated": "Average slippage per trade",
      "impact_on_returns": "Returns with and without slippage"
    }}
  }},
  "benchmark_comparison": {{
    "alpha": {{
      "formula": "portfolio_return - (rf + beta * (market_return - rf))",
      "description": "Excess return over CAPM expectation"
    }},
    "beta": {{
      "formula": "covariance(returns, market_returns) / variance(market_returns)",
      "description": "Market sensitivity"
    }},
    "tracking_error": {{
      "formula": "(returns - benchmark_returns).std() * sqrt(252)",
      "description": "Standard deviation of active returns"
    }},
    "correlation": {{
      "with_spy": "Correlation with S&P 500",
      "with_bonds": "Correlation with AGG",
      "with_factors": ["Value", "Momentum", "Quality"]
    }}
  }},
  "regime_analysis": {{
    "bull_market_performance": {{
      "definition": "SPY return > 20% annually",
      "metrics": ["return", "sharpe", "max_dd"]
    }},
    "bear_market_performance": {{
      "definition": "SPY return < -20% annually",
      "metrics": ["return", "sharpe", "max_dd"]
    }},
    "high_volatility_performance": {{
      "definition": "VIX > 30",
      "metrics": ["return", "sharpe", "win_rate"]
    }}
  }},
  "visualization_requirements": [
    "Cumulative returns vs benchmark",
    "Drawdown chart",
    "Rolling Sharpe ratio",
    "Monthly returns heatmap",
    "Position exposure over time",
    "Trade distribution histogram"
  ]
}}

Ensure metrics align with investment goals and provide comprehensive evaluation."""

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
            evaluation_metrics = json.loads(response)
        except json.JSONDecodeError:
            evaluation_metrics = {
                "description": response,
                "return_metrics": {"total_return": "Basic return calculation"},
                "risk_metrics": {"max_drawdown": "Maximum loss"}
            }
    except Exception as e:
        print(f"Error defining metrics: {e}")
        evaluation_metrics = {"error": str(e)}
    
    # Save metrics specification
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "experiment", "evaluation_metrics.json"), "w") as f:
        json.dump(evaluation_metrics, f, indent=2)
    
    # Update state
    state["evaluation_metrics"] = evaluation_metrics
    
    print("Evaluation metrics defined")
    
    return state