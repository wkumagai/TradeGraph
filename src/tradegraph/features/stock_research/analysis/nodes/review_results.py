"""Node for reviewing overall results and providing final recommendations."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def review_results_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Review all results and provide final recommendations.
    
    This node synthesizes all analysis and provides a final verdict.
    """
    performance_analysis = state.get("performance_analysis", {})
    strategy_evaluation = state.get("strategy_evaluation", {})
    key_insights = state.get("key_insights", [])
    improvement_suggestions = state.get("improvement_suggestions", [])
    investment_method = state.get("investment_method", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Provide a comprehensive final review of this trading strategy research.

Strategy: {investment_method.get('method_name', 'Unknown')}

Performance Summary:
{json.dumps(performance_analysis.get('overall_assessment', {}), indent=2)}

Viability Assessment:
{json.dumps(strategy_evaluation.get('viability_assessment', {}), indent=2)}

Key Insights:
{json.dumps(key_insights[:5], indent=2)}

Create a final review document with:

# Executive Summary
- One paragraph overview of the strategy and results
- Overall recommendation: IMPLEMENT / REFINE / ABANDON
- Confidence level: HIGH / MEDIUM / LOW

# Strategy Performance
- Achieved returns vs expectations
- Risk-adjusted performance assessment
- Comparison to benchmarks

# Key Strengths
1. [Specific strength with evidence]
2. [Specific strength with evidence]
3. [Specific strength with evidence]

# Critical Weaknesses
1. [Specific weakness with impact]
2. [Specific weakness with impact]
3. [Specific weakness with impact]

# Implementation Roadmap
## Phase 1: Preparation (Weeks 1-2)
- [ ] Task 1
- [ ] Task 2

## Phase 2: Paper Trading (Weeks 3-6)
- [ ] Task 1
- [ ] Task 2

## Phase 3: Limited Live Trading (Weeks 7-12)
- [ ] Task 1
- [ ] Task 2

## Phase 4: Full Implementation (Month 4+)
- [ ] Task 1
- [ ] Task 2

# Risk Management Framework
- Position sizing rules
- Stop loss methodology
- Portfolio limits
- Monitoring requirements

# Success Metrics
- KPIs to track
- Review frequency
- Adjustment triggers

# Final Verdict
Clear recommendation with reasoning and confidence level.

Be honest, specific, and actionable in the review."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        final_review = response.choices[0].message.content
    except Exception as e:
        print(f"Error creating final review: {e}")
        final_review = f"Error generating final review: {e}"
    
    # Save final review
    save_dir = state.get("save_dir", "./stock_research_output")
    
    # Save as markdown
    with open(os.path.join(save_dir, "analysis", "final_review.md"), "w") as f:
        f.write(final_review)
    
    # Create summary JSON
    review_summary = {
        "strategy_name": investment_method.get('method_name', 'Unknown'),
        "overall_recommendation": strategy_evaluation.get('recommendation', {}).get('action', 'Unknown'),
        "confidence_level": strategy_evaluation.get('recommendation', {}).get('confidence', 'Unknown'),
        "viability": strategy_evaluation.get('viability_assessment', {}).get('overall_viability', 'Unknown'),
        "performance_grade": performance_analysis.get('overall_assessment', {}).get('performance_grade', 'Unknown'),
        "key_metrics": {
            "total_return": state.get('performance_metrics', {}).get('total_return', 'N/A'),
            "sharpe_ratio": state.get('performance_metrics', {}).get('sharpe_ratio', 'N/A'),
            "max_drawdown": state.get('performance_metrics', {}).get('max_drawdown', 'N/A')
        },
        "next_steps": improvement_suggestions[:3]
    }
    
    with open(os.path.join(save_dir, "analysis", "review_summary.json"), "w") as f:
        json.dump(review_summary, f, indent=2)
    
    print("Final review completed")
    
    return state