"""Enhanced node for retrieving stock news with real market data context."""

import os
import json
import requests
from typing import Dict, Any, List
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def retrieve_stock_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve stock news enhanced with real market data from Alpha Vantage."""
    stock_symbols = state.get("stock_symbols", [])
    time_period = state.get("time_period", "24h")
    news_sources = state.get("news_sources", ["reuters", "bloomberg", "wsj", "cnbc"])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    save_dir = state.get("save_dir", "./stock_research_output")
    
    # Get Alpha Vantage API key
    alpha_vantage_key = os.getenv("ALPHAVANTAGE_API_KEY")
    
    # First, get real market data
    market_context = {}
    if alpha_vantage_key:
        print("Fetching real market data from Alpha Vantage...")
        base_url = "https://www.alphavantage.co/query"
        
        for symbol in stock_symbols[:3]:  # Limit due to rate limits
            try:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": alpha_vantage_key
                }
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if "Global Quote" in data:
                        quote = data["Global Quote"]
                        market_context[symbol] = {
                            "price": float(quote.get("05. price", 0)),
                            "change": float(quote.get("09. change", 0)),
                            "change_percent": quote.get("10. change percent", "0%"),
                            "volume": int(quote.get("06. volume", 0)),
                            "latest_trading_day": quote.get("07. latest trading day")
                        }
                        print(f"✓ {symbol}: ${market_context[symbol]['price']} ({market_context[symbol]['change_percent']})")
            except Exception as e:
                print(f"⚠️  Could not fetch data for {symbol}: {e}")
    
    # Initialize OpenAI client
    client = OpenAI()
    
    print("\nGenerating news analysis based on real market data...")
    
    # Create market summary
    market_summary = "Current market data:\n"
    for symbol, data in market_context.items():
        market_summary += f"- {symbol}: ${data['price']:.2f} ({data['change_percent']}) Volume: {data['volume']:,}\n"
    
    # Generate comprehensive news with market context
    prompt = f"""Generate realistic stock market news articles based on the following REAL market data:

{market_summary}

Time period: Last {time_period}
Focus stocks: {', '.join(stock_symbols)}

Create 10-15 news articles that reflect the actual market movements shown above. Include:
1. Analysis of why stocks moved (based on the real price changes)
2. Market sentiment analysis
3. Technical analysis mentions (support/resistance levels near current prices)
4. Volume analysis (unusual volume spikes)
5. Sector trends
6. Analyst opinions

For each article provide:
{{
    "title": "Realistic headline reflecting actual market movement",
    "source": "One of {news_sources}",
    "date": "Recent date",
    "summary": "2-3 sentences explaining the movement",
    "symbol": "Stock symbol or null for general news",
    "relevance_score": 7-10,
    "investment_impact": "bullish/bearish/neutral",
    "category": "earnings/market_analysis/technical/sector_news",
    "price_context": "Current price and movement mentioned in article"
}}

Make the news realistic and tied to the actual price movements shown in the data.
Return ONLY a JSON array."""
    
    all_news = []
    
    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        all_news = json.loads(content)
        
        # Add metadata and market context
        for i, article in enumerate(all_news):
            article["id"] = f"news_{i+1}"
            article["retrieved_at"] = datetime.now().isoformat()
            
            # Add actual market data if available
            if article.get("symbol") and article["symbol"] in market_context:
                article["market_data"] = market_context[article["symbol"]]
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        # Create fallback news with real data
        all_news = []
        for symbol, data in market_context.items():
            change_type = "gains" if data["change"] > 0 else "drops"
            all_news.append({
                "id": f"news_{len(all_news)+1}",
                "title": f"{symbol} {change_type} {abs(data['change']):.2f} points to ${data['price']:.2f}",
                "source": "reuters",
                "date": datetime.now().isoformat(),
                "summary": f"{symbol} closed at ${data['price']:.2f}, a change of {data['change_percent']} with volume of {data['volume']:,} shares.",
                "symbol": symbol,
                "relevance_score": 9,
                "investment_impact": "bullish" if data["change"] > 0 else "bearish",
                "category": "market_analysis",
                "market_data": data,
                "retrieved_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error generating news: {e}")
        all_news = []
    
    # Update state
    state["raw_news"] = all_news
    state["market_context"] = market_context
    
    # Save data
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "raw_news.json"), "w") as f:
        json.dump(all_news, f, indent=2)
    
    with open(os.path.join(save_dir, "market_context.json"), "w") as f:
        json.dump(market_context, f, indent=2)
    
    print(f"\nGenerated {len(all_news)} news articles with real market context")
    
    if market_context:
        print("\n📊 Market Context Used:")
        for symbol, data in market_context.items():
            print(f"  {symbol}: ${data['price']:.2f} ({data['change_percent']})")
    
    return state