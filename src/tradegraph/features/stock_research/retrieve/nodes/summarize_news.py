"""Node for summarizing filtered stock news."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def summarize_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize the filtered news into actionable insights.
    
    This node creates a comprehensive summary of the most important news
    and their potential impact on investment strategies.
    """
    filtered_news = state.get("filtered_news", [])
    stock_symbols = state.get("stock_symbols", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    if not filtered_news:
        state["news_summary"] = "No relevant news found for the specified criteria."
        return state
    
    client = OpenAI()
    
    # Prepare news for summarization
    news_text = json.dumps(filtered_news, indent=2)
    
    prompt = f"""Create a comprehensive investment-focused summary of the following stock market news.

Target stocks: {', '.join(stock_symbols[:10])}

Filtered news:
{news_text}

Create a structured summary with the following sections:

## Market Overview
- Current market sentiment and trends
- Key macroeconomic factors

## Individual Stock Analysis
For each relevant stock symbol:
- Recent news and events
- Analyst opinions and price targets
- Technical indicators mentioned
- Potential risks and opportunities

## Investment Opportunities
- Stocks showing bullish signals
- Potential value plays
- Momentum trades
- Contrarian opportunities

## Risk Factors
- Market-wide risks
- Sector-specific concerns
- Individual stock risks

## Actionable Insights
- Immediate action items
- Stocks to watch
- Entry/exit points mentioned
- Timing considerations

## Market Anomalies
- Unusual trading patterns
- Divergences from historical norms
- Potential arbitrage opportunities

Format the summary in clear, concise bullet points with specific data points when available."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        news_summary = response.choices[0].message.content
    except Exception as e:
        print(f"Error creating summary: {e}")
        news_summary = f"Summary generation failed. Found {len(filtered_news)} relevant articles."
    
    # Update state
    state["news_summary"] = news_summary
    
    # Save summary
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "news_summary.md"), "w") as f:
        f.write(news_summary)
    
    # Also save a combined report
    report = f"""# Stock Market News Analysis

## Analysis Date
{state.get('analysis_date', 'Current')}

## Target Stocks
{', '.join(stock_symbols)}

## Time Period
{state.get('time_period', '24h')}

---

{news_summary}

---

## Raw Data
- Total articles retrieved: {len(state.get('raw_news', []))}
- Relevant articles: {len(filtered_news)}
- News sources: {', '.join(state.get('news_sources', []))}
"""
    
    with open(os.path.join(save_dir, "news_analysis_report.md"), "w") as f:
        f.write(report)
    
    print("News summary completed")
    
    return state