"""Node for filtering relevant stock news."""

import os
import json
from typing import Dict, Any, List
from openai import OpenAI


def filter_relevant_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Filter news articles for relevance to investment decisions.
    
    This node analyzes the retrieved news and filters out less relevant articles,
    prioritizing news that could impact investment strategies.
    """
    raw_news = state.get("raw_news", [])
    stock_symbols = state.get("stock_symbols", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    if not raw_news:
        state["filtered_news"] = []
        return state
    
    client = OpenAI()
    
    # Prepare news for analysis
    news_text = json.dumps(raw_news[:50], indent=2)  # Limit to first 50 articles
    
    prompt = f"""Analyze the following stock market news and filter for investment relevance.

Stock symbols of interest: {', '.join(stock_symbols[:10])}

News articles:
{news_text}

Filter the news based on these criteria:
1. High relevance to investment decisions (score 8-10/10)
2. Potential market impact (earnings, Fed decisions, major events)
3. Actionable information (buy/sell signals, analyst upgrades/downgrades)
4. Recent anomalies or unusual market behavior
5. Sector-wide trends that could create opportunities

For each relevant article, provide:
- title: Original title
- source: News source
- date: Publication date
- symbol: Related stock symbol(s)
- relevance_score: 1-10 scale
- investment_impact: "bullish", "bearish", or "neutral"
- key_insights: Main takeaways for investors
- action_items: Potential investment actions

Return as a JSON array of the most relevant articles (max 20)."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # Parse the filtered news
        try:
            filtered_news = json.loads(content)
            if not isinstance(filtered_news, list):
                filtered_news = []
        except json.JSONDecodeError:
            # Fallback: keep all news with basic filtering
            filtered_news = [
                article for article in raw_news[:20]
                if any(symbol.upper() in str(article).upper() for symbol in stock_symbols)
                or any(keyword in str(article).lower() 
                      for keyword in ["earnings", "forecast", "analyst", "upgrade", "downgrade", 
                                     "fed", "interest rate", "inflation", "recession"])
            ]
    except Exception as e:
        print(f"Error filtering news: {e}")
        filtered_news = raw_news[:20]  # Keep top 20 as fallback
    
    # Update state
    state["filtered_news"] = filtered_news
    
    # Save filtered news
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "filtered_news.json"), "w") as f:
        json.dump(filtered_news, f, indent=2)
    
    print(f"Filtered to {len(filtered_news)} relevant news articles")
    
    return state