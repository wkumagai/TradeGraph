"""Node for summarizing investment research papers."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def summarize_investment_papers_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create a comprehensive summary of investment research papers.
    
    This node synthesizes insights from multiple papers to identify
    promising investment strategies and methods.
    """
    paper_contents = state.get("paper_contents", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    if not paper_contents:
        state["paper_summaries"] = []
        return state
    
    client = OpenAI()
    
    # First, create individual summaries
    paper_summaries = []
    
    for paper in paper_contents[:5]:  # Limit to avoid token limits
        prompt = f"""Create an investment-focused summary of this research paper:

Title: {paper.get('title', '')}
Authors: {', '.join(paper.get('authors', []))}
Abstract: {paper.get('abstract', '')}
Analysis: {json.dumps(paper.get('analysis', {}), indent=2)}

Create a structured summary covering:
1. Investment Strategy: What trading/investment approach is proposed?
2. Key Innovation: What's new compared to existing methods?
3. Performance: What returns/Sharpe ratio/metrics are reported?
4. Implementation: How can this be implemented in practice?
5. Data Requirements: What data is needed?
6. Risks: What are the main risks or limitations?
7. Market Conditions: When does this strategy work best?
8. Scalability: Can this handle large portfolios?

Be specific and quantitative where possible."""

        try:
            response = client.chat.completions.create(
                model=llm_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            summary = response.choices[0].message.content
            paper_summaries.append({
                "title": paper.get("title", ""),
                "summary": summary,
                "url": paper.get("url", ""),
                "published": paper.get("published", "")
            })
        except Exception as e:
            print(f"Error summarizing paper: {e}")
    
    # Create overall synthesis
    all_summaries_text = "\n\n---\n\n".join([
        f"**{s['title']}**\n{s['summary']}" 
        for s in paper_summaries
    ])
    
    synthesis_prompt = f"""Synthesize insights from these investment research papers to identify the most promising strategies:

{all_summaries_text}

Create a comprehensive report with:

# Investment Strategy Synthesis

## 1. Emerging Trends
- What new approaches are researchers exploring?
- Common themes across papers

## 2. Most Promising Strategies
Rank the top 5 strategies by potential, including:
- Strategy description
- Expected returns/Sharpe ratio
- Implementation complexity
- Required resources

## 3. Market Anomalies Identified
- New inefficiencies discovered
- Arbitrage opportunities
- Behavioral biases to exploit

## 4. Technology Applications
- ML/AI techniques that show promise
- Data sources being leveraged
- Computational requirements

## 5. Risk Considerations
- Common failure modes
- Market regime dependencies
- Overfitting concerns

## 6. Implementation Roadmap
- Which strategies to test first
- Required infrastructure
- Backtesting approach

## 7. Research Gaps
- Areas needing more research
- Potential improvements to existing methods

Be specific and actionable."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.5,
            max_tokens=2000
        )
        
        synthesis = response.choices[0].message.content
    except Exception as e:
        print(f"Error creating synthesis: {e}")
        synthesis = "Synthesis generation failed."
    
    # Update state
    state["paper_summaries"] = paper_summaries
    
    # Save summaries and synthesis
    save_dir = state.get("save_dir", "./stock_research_output")
    
    with open(os.path.join(save_dir, "paper_summaries.json"), "w") as f:
        json.dump(paper_summaries, f, indent=2)
    
    # Create comprehensive report
    report = f"""# Investment Research Papers Analysis

## Analysis Date
{state.get('analysis_date', 'Current')}

## Papers Analyzed
{len(paper_contents)} papers from the last {state.get('time_range', '1y')}

---

# Research Synthesis

{synthesis}

---

# Individual Paper Summaries

"""
    
    for summary in paper_summaries:
        report += f"""
## {summary['title']}
*Published: {summary['published']}*
[Link]({summary['url']})

{summary['summary']}

---
"""
    
    with open(os.path.join(save_dir, "investment_research_report.md"), "w") as f:
        f.write(report)
    
    print("Investment papers summary completed")
    
    return state