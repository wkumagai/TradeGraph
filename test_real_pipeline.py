#!/usr/bin/env python3
"""Test real data pipeline components without langgraph dependency."""

import os
import sys
import json
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
import time

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from airas.services.api_client.arxiv_client import ArxivClient
from airas.services.api_client.alpha_vantage_api import AlphaVantageClient
from openai import OpenAI
import feedparser


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
                "pubDate": item.findtext("pubDate", ""),
                "guid": item.findtext("guid", "")
            }
            entries.append(entry)
        
        return entries
    except Exception as e:
        print(f"   Error parsing RSS: {e}")
        return []


def test_real_news_retrieval(symbols):
    """Test real news retrieval from Yahoo Finance RSS."""
    print("\n" + "=" * 60)
    print("📰 Testing REAL News Retrieval (Yahoo Finance RSS)")
    print("=" * 60)
    
    all_news = []
    
    for symbol in symbols:
        print(f"\n📈 Fetching news for {symbol}...")
        
        try:
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}"
            entries = parse_rss_feed(rss_url)
            
            if entries:
                print(f"   ✓ Found {len(entries)} news items")
                
                for i, entry in enumerate(entries[:5]):
                    news_item = {
                        "id": f"news_{symbol}_{i+1}",
                        "title": entry.get("title", ""),
                        "source": "Yahoo Finance RSS",
                        "date": entry.get("pubDate", ""),
                        "url": entry.get("link", ""),
                        "symbol": symbol,
                        "data_source": "REAL"
                    }
                    all_news.append(news_item)
                    
                    if i < 3:
                        print(f"   • {news_item['title'][:80]}...")
            else:
                print(f"   ⚠️  No news found for {symbol}")
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    return all_news


def test_real_papers_retrieval():
    """Test real paper retrieval from ArXiv."""
    print("\n" + "=" * 60)
    print("📚 Testing REAL Paper Retrieval (ArXiv API)")
    print("=" * 60)
    
    client = ArxivClient()
    queries = [
        "stock market prediction machine learning",
        "portfolio optimization deep learning",
        "algorithmic trading neural network"
    ]
    
    all_papers = []
    
    for query in queries:
        print(f"\nSearching: '{query}'")
        
        try:
            xml_response = client.search_papers(
                query=query,
                max_results=3,
                sort_by="relevance"
            )
            
            feed = feedparser.parse(xml_response)
            print(f"   ✓ Found {len(feed.entries)} papers")
            
            for entry in feed.entries:
                paper = {
                    "title": entry.title.replace("\n", " ").strip(),
                    "authors": [author.name for author in entry.authors],
                    "published": entry.published,
                    "arxiv_id": entry.id.split("/abs/")[-1],
                    "summary": entry.summary.replace("\n", " ").strip()[:200] + "...",
                    "data_source": "REAL"
                }
                all_papers.append(paper)
                print(f"   • {paper['title'][:80]}...")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    return all_papers


def test_real_stock_data(symbols):
    """Test real stock data retrieval from Alpha Vantage."""
    print("\n" + "=" * 60)
    print("💹 Testing REAL Stock Data (Alpha Vantage API)")
    print("=" * 60)
    
    client = AlphaVantageClient()
    stock_data = []
    
    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")
        
        try:
            # Get quote data
            quote = client.get_quote(symbol)
            if quote:
                data = {
                    "symbol": symbol,
                    "price": quote.get("05. price", "N/A"),
                    "volume": quote.get("06. volume", "N/A"),
                    "latest_trading_day": quote.get("07. latest trading day", "N/A"),
                    "previous_close": quote.get("08. previous close", "N/A"),
                    "change": quote.get("09. change", "N/A"),
                    "change_percent": quote.get("10. change percent", "N/A"),
                    "data_source": "REAL"
                }
                stock_data.append(data)
                
                print(f"   ✓ Price: ${data['price']}")
                print(f"   ✓ Change: {data['change']} ({data['change_percent']})")
                print(f"   ✓ Volume: {data['volume']}")
            else:
                print("   ⚠️  No data received")
            
            # Rate limiting for Alpha Vantage
            time.sleep(12)
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    return stock_data


def test_real_ai_analysis(news_data, paper_data, stock_data):
    """Test real AI analysis using OpenAI."""
    print("\n" + "=" * 60)
    print("🤖 Testing REAL AI Analysis (OpenAI API)")
    print("=" * 60)
    
    try:
        client = OpenAI()
        
        # Prepare context
        context = f"""
Based on the following REAL data:

Stock Data:
{json.dumps(stock_data[:2], indent=2)}

Recent News Headlines:
{json.dumps([{"title": n["title"]} for n in news_data[:5]], indent=2)}

Academic Papers:
{json.dumps([{"title": p["title"]} for p in paper_data[:2]], indent=2)}

Create a simple momentum-based trading strategy.
"""
        
        print("Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a quantitative trading strategist."},
                {"role": "user", "content": context}
            ],
            max_tokens=500
        )
        
        strategy = response.choices[0].message.content
        print("\n✓ AI Strategy Generated:")
        print("-" * 40)
        print(strategy[:300] + "...")
        
        return {
            "strategy": strategy,
            "model": "gpt-4o-mini",
            "data_source": "REAL"
        }
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return None


def main():
    """Run complete real data test."""
    print("=" * 80)
    print("🚀 AIRAS-Trade REAL DATA TEST")
    print("=" * 80)
    print("Testing all components with REAL data sources...")
    
    # Test stocks
    symbols = ["AAPL", "NVDA", "MSFT"]
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"real_data_test_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Run tests
    results = {
        "timestamp": timestamp,
        "mode": "REAL DATA ONLY"
    }
    
    # 1. Test news
    news_data = test_real_news_retrieval(symbols)
    results["news"] = {
        "count": len(news_data),
        "source": "Yahoo Finance RSS",
        "type": "REAL"
    }
    
    # 2. Test papers
    paper_data = test_real_papers_retrieval()
    results["papers"] = {
        "count": len(paper_data),
        "source": "ArXiv API",
        "type": "REAL"
    }
    
    # 3. Test stock data
    stock_data = test_real_stock_data(symbols)
    results["stocks"] = {
        "count": len(stock_data),
        "source": "Alpha Vantage API",
        "type": "REAL"
    }
    
    # 4. Test AI analysis
    ai_result = test_real_ai_analysis(news_data, paper_data, stock_data)
    results["ai_analysis"] = {
        "generated": ai_result is not None,
        "source": "OpenAI API",
        "type": "REAL"
    }
    
    # Save all data
    with open(os.path.join(output_dir, "news_data.json"), "w") as f:
        json.dump(news_data, f, indent=2)
    
    with open(os.path.join(output_dir, "paper_data.json"), "w") as f:
        json.dump(paper_data, f, indent=2)
    
    with open(os.path.join(output_dir, "stock_data.json"), "w") as f:
        json.dump(stock_data, f, indent=2)
    
    if ai_result:
        with open(os.path.join(output_dir, "ai_strategy.json"), "w") as f:
            json.dump(ai_result, f, indent=2)
    
    with open(os.path.join(output_dir, "test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ REAL DATA TEST COMPLETED")
    print("=" * 80)
    print(f"\n📁 Output saved to: {output_dir}")
    print("\n📊 Summary:")
    print(f"   • News articles: {results['news']['count']} (REAL)")
    print(f"   • Academic papers: {results['papers']['count']} (REAL)")
    print(f"   • Stock quotes: {results['stocks']['count']} (REAL)")
    print(f"   • AI analysis: {'✓' if results['ai_analysis']['generated'] else '✗'} (REAL)")
    print("\n📌 All data is REAL - No mocks or simulations!")


if __name__ == "__main__":
    main()