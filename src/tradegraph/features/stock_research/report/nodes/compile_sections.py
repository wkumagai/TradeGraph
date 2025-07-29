"""Node for compiling report sections from all research phases."""

import os
import json
from typing import Dict, Any
from datetime import datetime


def compile_sections_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Compile all research outputs into organized report sections.
    
    This node structures content from all phases into a coherent report.
    """
    # Extract all components
    news_summary = state.get("news_summary", "No news summary available")
    paper_summaries = state.get("paper_summaries", [])
    investment_method = state.get("investment_method", {})
    market_anomaly = state.get("market_anomaly", {})
    trading_strategy = state.get("trading_strategy", {})
    experiment_design = state.get("experiment_design", {})
    performance_metrics = state.get("performance_metrics", {})
    performance_analysis = state.get("performance_analysis", {})
    strategy_evaluation = state.get("strategy_evaluation", {})
    key_insights = state.get("key_insights", [])
    
    # Compile report sections
    report_sections = {}
    
    # 1. Executive Summary
    report_sections["executive_summary"] = f"""## Executive Summary

**Date:** {datetime.now().strftime('%Y-%m-%d')}

**Strategy:** {investment_method.get('method_name', 'Unnamed Strategy')}

**Overall Recommendation:** {strategy_evaluation.get('recommendation', {}).get('action', 'Under Review')}

**Performance Summary:**
- Total Return: {performance_metrics.get('total_return', 'N/A')}
- Sharpe Ratio: {performance_metrics.get('sharpe_ratio', 'N/A')}
- Maximum Drawdown: {performance_metrics.get('max_drawdown', 'N/A')}
- Win Rate: {performance_metrics.get('win_rate', 'N/A')}

**Key Finding:** {key_insights[0] if key_insights else 'Analysis in progress'}
"""

    # 2. Market Research
    report_sections["market_research"] = f"""## Market Research

### Current Market Conditions
{news_summary}

### Academic Research Insights
Found {len(paper_summaries)} relevant research papers on investment strategies.

Key findings from recent research:
"""
    
    for i, paper in enumerate(paper_summaries[:3], 1):
        report_sections["market_research"] += f"\n{i}. **{paper.get('title', 'Untitled')}**\n"
        report_sections["market_research"] += f"   - {paper.get('summary', 'No summary')[:200]}...\n"

    # 3. Investment Strategy
    report_sections["investment_strategy"] = f"""## Investment Strategy

### Method Overview
{investment_method.get('executive_summary', 'No summary available')}

### Market Anomaly Exploited
**Anomaly:** {market_anomaly.get('anomaly_name', 'Not specified')}
**Type:** {market_anomaly.get('anomaly_type', 'Unknown')}

{market_anomaly.get('description', 'No description available')}

### Trading Rules
**Strategy Type:** {trading_strategy.get('strategy_type', 'Not specified')}

**Entry Conditions:**
{json.dumps(trading_strategy.get('entry_rules', {}).get('conditions', []), indent=2)}

**Exit Conditions:**
{json.dumps(trading_strategy.get('exit_rules', {}), indent=2)}

**Risk Management:**
{json.dumps(trading_strategy.get('risk_management', {}), indent=2)}
"""

    # 4. Backtest Results
    report_sections["backtest_results"] = f"""## Backtest Results

### Experiment Design
{experiment_design.get('experiment_name', 'Standard Backtest')}

**Methodology:** {experiment_design.get('methodology', {}).get('backtest_approach', {}).get('type', 'Not specified')}

### Performance Metrics
"""
    
    # Add performance metrics table
    metrics_table = "| Metric | Value |\n|--------|-------|\n"
    for metric, value in performance_metrics.items():
        if isinstance(value, (int, float, str)):
            metrics_table += f"| {metric.replace('_', ' ').title()} | {value} |\n"
    
    report_sections["backtest_results"] += metrics_table

    # 5. Analysis and Insights
    report_sections["analysis"] = f"""## Analysis and Insights

### Performance Assessment
{performance_analysis.get('overall_assessment', {}).get('performance_grade', 'Not graded')}

**Key Strengths:**
"""
    
    strengths = performance_analysis.get('overall_assessment', {}).get('key_strengths', [])
    for strength in strengths[:3]:
        report_sections["analysis"] += f"- {strength}\n"
    
    report_sections["analysis"] += "\n**Key Weaknesses:**\n"
    weaknesses = performance_analysis.get('overall_assessment', {}).get('key_weaknesses', [])
    for weakness in weaknesses[:3]:
        report_sections["analysis"] += f"- {weakness}\n"

    report_sections["analysis"] += "\n### Key Insights\n"
    for i, insight in enumerate(key_insights[:5], 1):
        report_sections["analysis"] += f"{i}. {insight}\n"

    # 6. Implementation Roadmap
    report_sections["implementation"] = f"""## Implementation Roadmap

### Viability Assessment
**Overall Viability:** {strategy_evaluation.get('viability_assessment', {}).get('overall_viability', 'Under Review')}
**Confidence Score:** {strategy_evaluation.get('viability_assessment', {}).get('confidence_score', 'N/A')}/100

### Next Steps
"""
    
    next_steps = strategy_evaluation.get('recommendation', {}).get('next_steps', [])
    for i, step in enumerate(next_steps[:5], 1):
        report_sections["implementation"] += f"{i}. {step}\n"
    
    report_sections["implementation"] += "\n### Required Improvements\n"
    improvements = strategy_evaluation.get('implementation_readiness', {}).get('required_improvements', [])
    for imp in improvements[:3]:
        report_sections["implementation"] += f"- **{imp.get('area', 'Area')}** ({imp.get('priority', 'medium')} priority): {imp.get('suggestion', 'No suggestion')}\n"

    # 7. Risk Disclosure
    report_sections["risk_disclosure"] = """## Risk Disclosure

**Important:** This research is for informational purposes only and does not constitute investment advice. Past performance does not guarantee future results. All trading strategies involve risk of loss.

### Key Risks
1. **Market Risk:** Strategy performance depends on market conditions
2. **Model Risk:** Backtested results may not reflect real-world performance
3. **Execution Risk:** Slippage and transaction costs may impact returns
4. **Liquidity Risk:** Large positions may face market impact
5. **Technology Risk:** System failures could affect strategy execution
"""

    # Save compiled sections
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(os.path.join(save_dir, "report"), exist_ok=True)
    
    with open(os.path.join(save_dir, "report", "report_sections.json"), "w") as f:
        json.dump(report_sections, f, indent=2)
    
    # Update state
    state["report_sections"] = report_sections
    
    print(f"Compiled {len(report_sections)} report sections")
    
    return state