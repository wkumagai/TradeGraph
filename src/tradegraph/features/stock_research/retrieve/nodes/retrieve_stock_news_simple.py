"""Simplified node for retrieving stock market news."""

import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from openai import OpenAI


def retrieve_stock_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve stock market news - simplified version with single API call."""
    stock_symbols = state.get("stock_symbols", [])
    time_period = state.get("time_period", "24h")
    news_sources = state.get("news_sources", ["reuters", "bloomberg", "wsj", "cnbc"])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    # Convert time period to date range
    time_map = {"24h": 1, "7d": 7, "30d": 30, "3m": 90, "1y": 365}
    days = time_map.get(time_period, 7)
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Initialize OpenAI client
    client = OpenAI()
    
    print("Generating simulated stock news data for testing...")
    
    # Single comprehensive prompt
    prompt = f"""Generate realistic stock market news articles for testing a stock investment research system.
    
    Create 10-15 news articles covering:
    1. General market news (3-4 articles)
    2. Specific news for stocks: {', '.join(stock_symbols[:3])} (2-3 articles each)
    3. Fed policy/interest rates (1-2 articles)
    4. Market volatility/trends (1-2 articles)
    
    Time period: {date_from} to today
    Sources: {news_sources}
    
    For each article provide ALL these fields:
    {{
        "title": "Realistic headline",
        "source": "One of the specified sources",
        "date": "ISO date within time period",
        "summary": "2-3 sentence summary",
        "symbol": "Stock symbol if specific, null if general",
        "relevance_score": 7-10,
        "investment_impact": "bullish/bearish/neutral",
        "category": "earnings/fed_policy/market_trend/company_news"
    }}
    
    Return ONLY a JSON array with no additional text."""
    
    all_news = []
    
    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        all_news = json.loads(content)
        
        # Add metadata
        for i, article in enumerate(all_news):
            article["id"] = f"news_{i+1}"
            article["retrieved_at"] = datetime.now().isoformat()
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        # Create minimal fallback data
        all_news = [{
            "id": "news_1",
            "title": "Market Update: Stocks Rise on Strong Earnings",
            "source": "reuters",
            "date": datetime.now().isoformat(),
            "summary": "US stocks rose today as companies reported better than expected earnings.",
            "symbol": None,
            "relevance_score": 8,
            "investment_impact": "bullish",
            "category": "market_trend",
            "retrieved_at": datetime.now().isoformat()
        }]
    except Exception as e:
        print(f"Error generating news: {e}")
        all_news = []
    
    # Update state
    state["raw_news"] = all_news
    
    # Save raw news
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "raw_news.json"), "w") as f:
        json.dump(all_news, f, indent=2)
    
    print(f"Generated {len(all_news)} simulated news articles")
    
    if len(all_news) > 0:
        print("\nNOTE: This is simulated data for testing.")
        print("For production, use real news APIs.")
    
    return state