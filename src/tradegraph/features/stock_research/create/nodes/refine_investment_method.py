"""Node for refining and finalizing the investment method."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def refine_investment_method_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Refine and integrate all components into a complete investment method.
    
    This node combines the investment idea, anomaly, and strategy into
    a coherent, implementable investment methodology.
    """
    investment_idea = state.get("investment_idea", "")
    market_anomaly = state.get("market_anomaly", {})
    trading_strategy = state.get("trading_strategy", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Refine and integrate all components into a complete, production-ready investment method.

Investment Idea:
{investment_idea}

Market Anomaly:
{json.dumps(market_anomaly, indent=2)}

Trading Strategy:
{json.dumps(trading_strategy, indent=2)}

Create a refined, complete investment method in JSON format with:

{{
  "method_name": "Final method name",
  "executive_summary": "2-3 paragraph overview suitable for investors",
  "theoretical_foundation": {{
    "core_thesis": "Central investment thesis",
    "academic_support": ["Key papers or theories"],
    "empirical_evidence": ["Historical validation"],
    "behavioral_rationale": "Why this inefficiency persists"
  }},
  "implementation_guide": {{
    "phase_1_setup": {{
      "infrastructure": ["Required systems and tools"],
      "data_sources": ["Specific vendors and APIs"],
      "initial_capital": "Minimum viable amount",
      "team_requirements": "Skills needed"
    }},
    "phase_2_testing": {{
      "paper_trading_period": "Recommended duration",
      "success_metrics": ["KPIs to monitor"],
      "go_live_criteria": ["Conditions to meet"]
    }},
    "phase_3_scaling": {{
      "position_sizing_progression": "How to scale up",
      "risk_limits_progression": "How to expand limits",
      "capacity_analysis": "Maximum strategy AUM"
    }}
  }},
  "risk_framework": {{
    "risk_factors": [
      {{
        "risk_type": "market/execution/model/liquidity",
        "description": "Specific risk",
        "mitigation": "How to manage",
        "monitoring": "Metrics to track"
      }}
    ],
    "stress_scenarios": ["Scenarios to test"],
    "contingency_plans": ["Actions for adverse events"]
  }},
  "performance_expectations": {{
    "base_case": {{
      "annual_return": "Expected %",
      "volatility": "Expected %",
      "sharpe_ratio": "Expected",
      "max_drawdown": "Expected %"
    }},
    "bull_market": {{}},
    "bear_market": {{}},
    "high_volatility": {{}}
  }},
  "monitoring_framework": {{
    "daily_metrics": ["What to track daily"],
    "weekly_review": ["Weekly analysis points"],
    "monthly_evaluation": ["Deep dive topics"],
    "red_flags": ["Warning signals to watch"]
  }},
  "evolution_plan": {{
    "research_priorities": ["Ongoing research areas"],
    "enhancement_ideas": ["Potential improvements"],
    "adaptation_triggers": ["When to modify strategy"]
  }},
  "competitive_analysis": {{
    "similar_strategies": ["Comparable approaches"],
    "our_edge": "What makes this unique",
    "defensibility": "How to maintain edge"
  }}
}}

Ensure the method is:
1. Immediately actionable
2. Robust and well-tested conceptually
3. Scalable but starts small
4. Clearly differentiated
5. Risk-aware and defensive

Provide a complete methodology document."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        response_text = response.choices[0].message.content
        # Try to parse as JSON
        try:
            investment_method = json.loads(response_text)
        except json.JSONDecodeError:
            # Create structured method from text
            investment_method = {
                "method_name": "Refined Investment Method",
                "executive_summary": response_text[:500],
                "full_description": response_text,
                "status": "Ready for implementation"
            }
    except Exception as e:
        print(f"Error refining method: {e}")
        investment_method = {
            "method_name": "Error",
            "description": "Failed to refine method",
            "error": str(e)
        }
    
    # Save the complete investment method
    save_dir = state.get("save_dir", "./stock_research_output")
    
    # Save as JSON
    with open(os.path.join(save_dir, "investment_method", "complete_method.json"), "w") as f:
        json.dump(investment_method, f, indent=2)
    
    # Create a comprehensive markdown report
    report = f"""# Investment Method: {investment_method.get('method_name', 'Generated Method')}

## Executive Summary
{investment_method.get('executive_summary', 'No summary available')}

## Investment Thesis
{investment_idea}

## Market Anomaly
**Type**: {market_anomaly.get('anomaly_type', 'Unknown')}
**Description**: {market_anomaly.get('description', 'No description')}

## Trading Strategy
**Name**: {trading_strategy.get('strategy_name', 'Unknown')}
**Type**: {trading_strategy.get('strategy_type', 'Unknown')}

## Implementation Details
{json.dumps(investment_method.get('implementation_guide', {}), indent=2)}

## Risk Management
{json.dumps(investment_method.get('risk_framework', {}), indent=2)}

## Performance Expectations
{json.dumps(investment_method.get('performance_expectations', {}), indent=2)}

---
*Generated by AIRAS-Trade Investment Research System*
"""
    
    with open(os.path.join(save_dir, "investment_method", "investment_method_report.md"), "w") as f:
        f.write(report)
    
    # Update state
    state["investment_method"] = investment_method
    
    print("Investment method refined and finalized")
    
    return state