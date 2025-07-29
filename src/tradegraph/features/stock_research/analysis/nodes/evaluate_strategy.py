"""Node for evaluating strategy effectiveness."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def evaluate_strategy_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate the trading strategy's effectiveness and viability.
    
    This node assesses whether the strategy is worth implementing.
    """
    performance_analysis = state.get("performance_analysis", {})
    performance_metrics = state.get("performance_metrics", {})
    trading_strategy = state.get("trading_strategy", {})
    market_anomaly = state.get("market_anomaly", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Evaluate this trading strategy's effectiveness and real-world viability.

Performance Analysis:
{json.dumps(performance_analysis, indent=2)}

Original Strategy:
{json.dumps(trading_strategy.get('strategy_name', ''), indent=2)}

Market Anomaly Exploited:
{json.dumps(market_anomaly.get('anomaly_name', ''), indent=2)}

Create a comprehensive strategy evaluation:

{{
  "viability_assessment": {{
    "overall_viability": "Highly Viable/Viable/Marginal/Not Viable",
    "confidence_score": 0-100,
    "reasoning": "Detailed explanation"
  }},
  "anomaly_validation": {{
    "anomaly_confirmed": true/false,
    "strength_assessment": "Strong/Moderate/Weak/Not Found",
    "persistence_likelihood": "High/Medium/Low",
    "explanation": "Does the backtest confirm the anomaly exists?"
  }},
  "implementation_readiness": {{
    "ready_for_production": true/false,
    "required_improvements": [
      {{"area": "risk management", "priority": "high", "suggestion": "..."}},
      {{"area": "execution", "priority": "medium", "suggestion": "..."}}
    ],
    "estimated_time_to_ready": "X weeks/months"
  }},
  "competitive_analysis": {{
    "uniqueness": "Highly Unique/Somewhat Unique/Common",
    "crowding_risk": "High/Medium/Low",
    "alpha_decay_estimate": "X% per year",
    "moat_assessment": "What protects this strategy?"
  }},
  "scalability_analysis": {{
    "minimum_capital": "$X for viable implementation",
    "optimal_capital": "$X-Y range",
    "capacity_limit": "$X maximum before degradation",
    "scaling_challenges": ["List of challenges"]
  }},
  "risk_assessment": {{
    "primary_risks": [
      {{"risk": "regime change", "impact": "high", "mitigation": "..."}}
    ],
    "black_swan_vulnerability": "High/Medium/Low",
    "correlation_risks": "Correlation to market/factors",
    "operational_risks": ["execution", "data", "technology"]
  }},
  "cost_benefit_analysis": {{
    "expected_net_return": "X% after all costs",
    "break_even_capital": "$X needed to cover costs",
    "cost_structure": {{
      "fixed_costs": "$X per year",
      "variable_costs": "X% of AUM",
      "total_expense_ratio": "X%"
    }}
  }},
  "recommendation": {{
    "action": "Implement/Test Further/Modify/Abandon",
    "confidence": "High/Medium/Low",
    "rationale": "Key reasons for recommendation",
    "next_steps": ["Ordered list of actions"]
  }}
}}

Provide honest, critical evaluation focused on real-world implementation."""

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
            strategy_evaluation = json.loads(response)
        except json.JSONDecodeError:
            strategy_evaluation = {
                "evaluation": response,
                "viability_assessment": {"overall_viability": "Pending"}
            }
    except Exception as e:
        print(f"Error evaluating strategy: {e}")
        strategy_evaluation = {"error": str(e)}
    
    # Save strategy evaluation
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "analysis", "strategy_evaluation.json"), "w") as f:
        json.dump(strategy_evaluation, f, indent=2)
    
    # Update state
    state["strategy_evaluation"] = strategy_evaluation
    
    print("Strategy evaluation completed")
    
    return state