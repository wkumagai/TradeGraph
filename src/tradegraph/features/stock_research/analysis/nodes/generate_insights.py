"""Node for generating actionable insights from analysis."""

import os
import json
from typing import Dict, Any, List
from openai import OpenAI


def generate_insights_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate actionable insights from the performance analysis.
    
    This node distills key findings and provides specific recommendations.
    """
    performance_analysis = state.get("performance_analysis", {})
    strategy_evaluation = state.get("strategy_evaluation", {})
    performance_metrics = state.get("performance_metrics", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Generate actionable insights from this trading strategy analysis.

Performance Analysis:
{json.dumps(performance_analysis, indent=2)}

Strategy Evaluation:
{json.dumps(strategy_evaluation, indent=2)}

Key Metrics Summary:
- Total Return: {performance_metrics.get('total_return', 'N/A')}
- Sharpe Ratio: {performance_metrics.get('sharpe_ratio', 'N/A')}
- Max Drawdown: {performance_metrics.get('max_drawdown', 'N/A')}
- Win Rate: {performance_metrics.get('win_rate', 'N/A')}

Generate comprehensive insights:

1. **Key Findings** (5-7 most important discoveries):
   - Finding: [Specific observation]
   - Implication: [What this means]
   - Action: [What to do about it]

2. **Success Factors** (What worked well):
   - Factor: [What contributed to success]
   - Evidence: [Specific metrics/results]
   - Leverage: [How to maximize this]

3. **Failure Points** (What didn't work):
   - Issue: [Specific problem]
   - Impact: [Quantified effect]
   - Solution: [How to address it]

4. **Market Insights** (What we learned about markets):
   - Insight: [Market behavior observation]
   - Reliability: [How consistent is this]
   - Application: [How to use this knowledge]

5. **Improvement Opportunities** (Specific enhancements):
   - Improvement: [Specific change]
   - Expected Impact: [Quantified benefit]
   - Implementation: [How to do it]
   - Priority: [High/Medium/Low]

6. **Risk Discoveries** (Unexpected risks found):
   - Risk: [Specific risk identified]
   - Frequency: [How often it occurs]
   - Mitigation: [How to manage it]

7. **Parameter Insights** (Optimal settings discovered):
   - Parameter: [Name]
   - Optimal Value: [Value]
   - Sensitivity: [How sensitive performance is]
   - Robustness: [Stable across conditions?]

Format insights to be specific, quantified, and immediately actionable."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        insights_response = response.choices[0].message.content
        
        # Parse the insights into structured format
        key_insights = []
        improvement_suggestions = []
        
        # Extract key insights (simplified parsing)
        lines = insights_response.split('\n')
        current_section = ""
        
        for line in lines:
            if "**Key Findings**" in line:
                current_section = "findings"
            elif "**Improvement Opportunities**" in line:
                current_section = "improvements"
            elif current_section == "findings" and "-" in line and ":" in line:
                key_insights.append(line.strip())
            elif current_section == "improvements" and "-" in line:
                # Try to parse improvement suggestions
                parts = line.split(":")
                if len(parts) >= 2:
                    improvement_suggestions.append({
                        "area": parts[0].replace("-", "").strip(),
                        "suggestion": ":".join(parts[1:]).strip(),
                        "priority": "medium"  # Default, could be extracted from text
                    })
        
        # Ensure we have some insights
        if not key_insights:
            key_insights = [
                f"Strategy achieved {performance_metrics.get('total_return', 'N/A')} return",
                f"Risk-adjusted performance (Sharpe): {performance_metrics.get('sharpe_ratio', 'N/A')}",
                f"Maximum drawdown: {performance_metrics.get('max_drawdown', 'N/A')}",
                "Further analysis needed for detailed insights"
            ]
        
        if not improvement_suggestions:
            improvement_suggestions = [
                {
                    "area": "Risk Management",
                    "suggestion": "Implement dynamic position sizing based on volatility",
                    "priority": "high"
                },
                {
                    "area": "Execution",
                    "suggestion": "Add slippage modeling for more realistic results",
                    "priority": "medium"
                }
            ]
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        key_insights = ["Error generating insights"]
        improvement_suggestions = [{"area": "Error", "suggestion": str(e)}]
        insights_response = f"Error: {e}"
    
    # Save insights
    save_dir = state.get("save_dir", "./stock_research_output")
    
    insights_document = {
        "full_insights": insights_response,
        "key_insights": key_insights,
        "improvement_suggestions": improvement_suggestions,
        "summary_metrics": {
            "total_return": performance_metrics.get('total_return', 'N/A'),
            "sharpe_ratio": performance_metrics.get('sharpe_ratio', 'N/A'),
            "max_drawdown": performance_metrics.get('max_drawdown', 'N/A'),
            "win_rate": performance_metrics.get('win_rate', 'N/A')
        }
    }
    
    with open(os.path.join(save_dir, "analysis", "insights.json"), "w") as f:
        json.dump(insights_document, f, indent=2)
    
    # Save readable insights document
    with open(os.path.join(save_dir, "analysis", "insights.md"), "w") as f:
        f.write(f"# Trading Strategy Insights\n\n{insights_response}")
    
    # Update state
    state["key_insights"] = key_insights
    state["improvement_suggestions"] = improvement_suggestions
    
    print(f"Generated {len(key_insights)} key insights and {len(improvement_suggestions)} improvement suggestions")
    
    return state