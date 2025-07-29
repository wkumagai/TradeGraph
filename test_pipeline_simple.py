#!/usr/bin/env python3
"""Simple test of real data pipeline without complex dependencies."""

import os
import json
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
# OpenAI import will be handled conditionally
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️  OpenAI module not available - AI analysis will be skipped")


def parse_rss_feed(url: str):
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
                "pubDate": item.findtext("pubDate", "")
            }
            entries.append(entry)
        
        return entries
    except Exception as e:
        print(f"   Error parsing RSS: {e}")
        return []


def search_arxiv(query: str, max_results: int = 5) -> list:
    """Search ArXiv and parse results."""
    base_url = "https://export.arxiv.org/api/query"
    
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        
        # Define namespaces
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            paper = {
                "title": entry.findtext('atom:title', '', ns).strip(),
                "summary": entry.findtext('atom:summary', '', ns).strip()[:200] + "...",
                "published": entry.findtext('atom:published', '', ns),
                "id": entry.findtext('atom:id', '', ns)
            }
            papers.append(paper)
        
        return papers
    except Exception as e:
        print(f"Error fetching from ArXiv: {e}")
        return []


def get_alpha_vantage_quote(symbol: str, api_key: str) -> dict:
    """Get real-time quote from Alpha Vantage."""
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read())
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            return {
                "symbol": symbol,
                "price": quote.get("05. price", "N/A"),
                "change": quote.get("09. change", "N/A"),
                "change_percent": quote.get("10. change percent", "N/A"),
                "volume": quote.get("06. volume", "N/A")
            }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    
    return {}


def main():
    """Run simple real data pipeline test."""
    print("=" * 80)
    print("🚀 AIRAS-Trade REAL DATA PIPELINE TEST (Simple Version)")
    print("=" * 80)
    
    # Load API key
    try:
        with open(".env", "r") as f:
            env_content = f.read()
        api_key = None
        for line in env_content.split("\n"):
            if "ALPHAVANTAGE_API_KEY" in line:
                api_key = line.split("=")[1].strip()
                break
    except:
        print("❌ Could not load .env file")
        return
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"real_pipeline_test_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Test symbols
    symbols = ["AAPL", "NVDA", "MSFT"]
    
    # 1. Test Yahoo Finance RSS News
    print("\n📰 1. Testing REAL News from Yahoo Finance RSS")
    print("=" * 60)
    
    all_news = []
    for symbol in symbols:
        print(f"\nFetching news for {symbol}...")
        rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}"
        entries = parse_rss_feed(rss_url)
        
        if entries:
            print(f"✓ Found {len(entries)} news items")
            for i, entry in enumerate(entries[:3]):
                print(f"  • {entry['title'][:80]}...")
                all_news.append({
                    "symbol": symbol,
                    "title": entry["title"],
                    "date": entry["pubDate"],
                    "source": "Yahoo Finance RSS"
                })
        time.sleep(1)
    
    # 2. Test ArXiv API
    print("\n📚 2. Testing REAL Papers from ArXiv API")
    print("=" * 60)
    
    queries = [
        "stock market prediction machine learning",
        "portfolio optimization neural network",
        "algorithmic trading strategy"
    ]
    
    all_papers = []
    for query in queries:
        print(f"\nSearching: '{query}'")
        papers = search_arxiv(query, max_results=3)
        
        if papers:
            print(f"✓ Found {len(papers)} papers")
            for paper in papers[:2]:
                print(f"  • {paper['title'][:80]}...")
                all_papers.append({
                    "title": paper["title"],
                    "summary": paper["summary"],
                    "source": "ArXiv API"
                })
    
    # 3. Test Alpha Vantage API
    print("\n💹 3. Testing REAL Stock Data from Alpha Vantage")
    print("=" * 60)
    
    stock_data = []
    for symbol in symbols:
        print(f"\nFetching {symbol}...")
        quote = get_alpha_vantage_quote(symbol, api_key)
        
        if quote:
            print(f"✓ {symbol}: ${quote['price']} ({quote['change_percent']})")
            stock_data.append(quote)
        
        time.sleep(12)  # Rate limiting
    
    # 4. Test OpenAI API (if available)
    strategy = None
    if HAS_OPENAI:
        print("\n🤖 4. Testing REAL AI Analysis with OpenAI")
        print("=" * 60)
        
        try:
            client = OpenAI()
            
            # Create simple prompt
            prompt = f"""Based on this REAL market data:

Stock Prices:
{json.dumps(stock_data, indent=2)}

Recent News Headlines:
{json.dumps([n["title"] for n in all_news[:5]], indent=2)}

Create a simple momentum trading strategy in 3 sentences."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a trading strategist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            
            strategy = response.choices[0].message.content
            print("\n✓ AI Strategy Generated:")
            print("-" * 40)
            print(strategy)
            
        except Exception as e:
            print(f"❌ OpenAI Error: {e}")
            strategy = None
    else:
        print("\n⚠️  4. Skipping OpenAI API test (module not available)")
    
    # Save all results
    results = {
        "timestamp": timestamp,
        "news_count": len(all_news),
        "paper_count": len(all_papers),
        "stock_count": len(stock_data),
        "ai_generated": strategy is not None,
        "all_sources": "REAL DATA ONLY"
    }
    
    with open(os.path.join(output_dir, "results.json"), "w") as f:
        json.dump({
            "summary": results,
            "news": all_news,
            "papers": all_papers,
            "stocks": stock_data,
            "strategy": strategy
        }, f, indent=2)
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ REAL DATA PIPELINE TEST COMPLETED")
    print("=" * 80)
    print(f"\n📁 Results saved to: {output_dir}")
    print("\n📊 Summary:")
    print(f"  • News articles: {len(all_news)} (Yahoo Finance RSS - REAL)")
    print(f"  • Academic papers: {len(all_papers)} (ArXiv API - REAL)")
    print(f"  • Stock quotes: {len(stock_data)} (Alpha Vantage - REAL)")
    print(f"  • AI strategy: {'✓' if strategy else '✗'} (OpenAI API - REAL)")
    print("\n📌 ALL DATA IS REAL - NO MOCKS OR SIMULATIONS!")


if __name__ == "__main__":
    main()