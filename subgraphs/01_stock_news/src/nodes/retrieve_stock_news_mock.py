"""Mock node for retrieving stock market news without API calls."""

import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


def retrieve_stock_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve stock market news - mock version for testing."""
    stock_symbols = state.get("stock_symbols", [])
    time_period = state.get("time_period", "24h")
    news_sources = state.get("news_sources", ["reuters", "bloomberg", "wsj", "cnbc"])
    
    # Convert time period to date range
    time_map = {"24h": 1, "7d": 7, "30d": 30, "3m": 90, "1y": 365}
    days = time_map.get(time_period, 7)
    
    print("Generating mock stock news data for testing...")
    
    # Generate mock news data
    all_news = []
    
    # General market news
    general_templates = [
        ("Fed Signals Potential Rate Cut in Coming Months", "Federal Reserve officials hinted at possible rate cuts as inflation shows signs of cooling.", "fed_policy", "neutral"),
        ("Stock Market Reaches New Highs Amid Strong Earnings", "Major indices hit record levels as corporate earnings exceed expectations.", "market_trend", "bullish"),
        ("Market Volatility Increases on Geopolitical Concerns", "Trading volumes surge as investors react to international tensions.", "market_trend", "bearish"),
        ("Tech Sector Leads Market Rally", "Technology stocks drive gains as AI innovation continues to attract investors.", "market_trend", "bullish")
    ]
    
    for i, (title, summary, category, impact) in enumerate(general_templates):
        news_date = (datetime.now() - timedelta(days=random.randint(0, days))).isoformat()
        all_news.append({
            "id": f"news_{i+1}",
            "title": title,
            "source": random.choice(news_sources),
            "date": news_date,
            "summary": summary,
            "symbol": None,
            "relevance_score": random.randint(7, 10),
            "investment_impact": impact,
            "category": category,
            "retrieved_at": datetime.now().isoformat()
        })
    
    # Stock-specific news
    stock_templates = [
        ("{symbol} Beats Earnings Expectations", "{symbol} reported quarterly earnings that exceeded analyst forecasts by 15%.", "earnings", "bullish"),
        ("Analysts Upgrade {symbol} to Buy", "Major investment firms raise price targets for {symbol} citing strong fundamentals.", "company_news", "bullish"),
        ("{symbol} Announces Stock Buyback Program", "{symbol} board approves $5 billion share repurchase program.", "company_news", "bullish"),
        ("{symbol} Faces Regulatory Scrutiny", "Government agencies investigate {symbol} over compliance issues.", "company_news", "bearish")
    ]
    
    for symbol in stock_symbols[:3]:
        for j in range(2):  # 2 articles per stock
            template = random.choice(stock_templates)
            title = template[0].format(symbol=symbol)
            summary = template[1].format(symbol=symbol)
            
            news_date = (datetime.now() - timedelta(days=random.randint(0, days))).isoformat()
            all_news.append({
                "id": f"news_{len(all_news)+1}",
                "title": title,
                "source": random.choice(news_sources),
                "date": news_date,
                "summary": summary,
                "symbol": symbol,
                "relevance_score": random.randint(8, 10),
                "investment_impact": template[3],
                "category": template[2],
                "price_target": f"${random.randint(100, 500)}" if "upgrade" in title.lower() else None,
                "analyst_rating": "buy" if "upgrade" in title.lower() else None,
                "retrieved_at": datetime.now().isoformat()
            })
    
    # Update state
    state["raw_news"] = all_news
    
    # Save raw news
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "raw_news.json"), "w") as f:
        json.dump(all_news, f, indent=2)
    
    print(f"Generated {len(all_news)} mock news articles")
    print("\nNOTE: This is mock data for testing pipeline functionality.")
    print("For production, implement real news API integration.")
    
    return state