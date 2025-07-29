"""Real stock market news retrieval using Yahoo Finance RSS."""

import os
import json
from typing import Dict, Any, List
from datetime import datetime
import time
import urllib.request
import xml.etree.ElementTree as ET


def parse_rss_feed(url: str) -> List[Dict[str, str]]:
    """Parse RSS feed and return list of entries."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        entries = []
        
        # Find all items in the RSS feed
        for item in root.findall(".//item"):
            entry = {
                "title": item.findtext("title", ""),
                "link": item.findtext("link", ""),
                "description": item.findtext("description", ""),
                "pubDate": item.findtext("pubDate", ""),
                "guid": item.findtext("guid", "")
            }
            entries.append(entry)
        
        return entries
    except Exception as e:
        print(f"   Error parsing RSS: {e}")
        return []


def retrieve_stock_news_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve real stock market news from Yahoo Finance RSS."""
    stock_symbols = state.get("stock_symbols", [])
    time_period = state.get("time_period", "24h")
    
    print("🔍 Retrieving REAL stock news from Yahoo Finance RSS...")
    print("=" * 60)
    
    all_news = []
    
    # Process each stock symbol
    for symbol in stock_symbols:
        print(f"\n📈 Fetching news for {symbol}...")
        
        try:
            # Yahoo Finance RSS URL
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}"
            
            # Parse RSS feed
            entries = parse_rss_feed(rss_url)
            
            if entries:
                print(f"   ✓ Found {len(entries)} news items")
                
                for i, entry in enumerate(entries[:10]):  # Limit to 10 per symbol
                    news_item = {
                        "id": f"news_{symbol}_{i+1}",
                        "title": entry.get("title", ""),
                        "source": "Yahoo Finance",
                        "date": entry.get("pubDate", datetime.now().isoformat()),
                        "summary": entry.get("description", ""),
                        "url": entry.get("link", ""),
                        "symbol": symbol,
                        "relevance_score": 9,  # High relevance as it's stock-specific
                        "category": "company_news",
                        "retrieved_at": datetime.now().isoformat(),
                        "data_source": "REAL - Yahoo Finance RSS"
                    }
                    
                    all_news.append(news_item)
                    
                    # Print first few titles
                    if i < 3:
                        print(f"   • {news_item['title'][:80]}...")
            else:
                print(f"   ⚠️  No news found for {symbol}")
            
            # Rate limit to avoid overwhelming the service
            time.sleep(1)
            
        except Exception as e:
            print(f"   ✗ Error fetching news for {symbol}: {e}")
    
    # Also get general market news
    print("\n📊 Fetching general market news...")
    try:
        market_symbols = ["^GSPC", "^DJI", "^IXIC"]  # S&P 500, Dow Jones, Nasdaq
        market_names = {"^GSPC": "S&P 500", "^DJI": "Dow Jones", "^IXIC": "Nasdaq"}
        
        for market_symbol in market_symbols:
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={market_symbol}"
            entries = parse_rss_feed(rss_url)
            
            if entries:
                for i, entry in enumerate(entries[:5]):  # 5 per index
                    news_item = {
                        "id": f"news_market_{market_symbol}_{i+1}",
                        "title": entry.get("title", ""),
                        "source": "Yahoo Finance",
                        "date": entry.get("pubDate", datetime.now().isoformat()),
                        "summary": entry.get("description", ""),
                        "url": entry.get("link", ""),
                        "symbol": None,
                        "market_index": market_names.get(market_symbol, market_symbol),
                        "relevance_score": 8,
                        "category": "market_trend",
                        "retrieved_at": datetime.now().isoformat(),
                        "data_source": "REAL - Yahoo Finance RSS"
                    }
                    all_news.append(news_item)
            
            time.sleep(1)
            
    except Exception as e:
        print(f"   ✗ Error fetching market news: {e}")
    
    # Update state
    state["raw_news"] = all_news
    
    # Save raw news
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(save_dir, exist_ok=True)
    
    news_file = os.path.join(save_dir, "raw_news_real.json")
    with open(news_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_articles": len(all_news),
            "data_source": "Yahoo Finance RSS - REAL DATA",
            "articles": all_news
        }, f, indent=2)
    
    print(f"\n✅ Retrieved {len(all_news)} REAL news articles")
    print(f"📁 Saved to: {news_file}")
    print("\n📌 This is REAL news data from Yahoo Finance RSS feeds")
    
    return state