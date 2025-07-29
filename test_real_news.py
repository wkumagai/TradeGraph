#!/usr/bin/env python3
"""Test real news retrieval from free news sources."""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_finviz_news(symbols: List[str]) -> List[Dict[str, Any]]:
    """Get real news from FinViz (free, no API key required)."""
    print("\nTesting FinViz news scraping...")
    print("=" * 40)
    
    all_news = []
    
    for symbol in symbols:
        print(f"\nFetching news for {symbol}...")
        
        try:
            # FinViz provides free news data through their website
            url = f"https://finviz.com/quote.ashx?t={symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML to extract news (simplified for demonstration)
                # In production, use BeautifulSoup
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find news table
                news_table = soup.find('table', {'id': 'news-table'})
                
                if news_table:
                    rows = news_table.find_all('tr')
                    
                    for row in rows[:5]:  # Get top 5 news
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            time_cell = cells[0].text.strip()
                            link_cell = cells[1].find('a')
                            
                            if link_cell:
                                news_item = {
                                    'symbol': symbol,
                                    'title': link_cell.text.strip(),
                                    'url': link_cell.get('href', ''),
                                    'time': time_cell,
                                    'source': 'FinViz',
                                    'date': datetime.now().strftime('%Y-%m-%d')
                                }
                                all_news.append(news_item)
                                print(f"   • {news_item['title'][:80]}...")
                
                print(f"   ✓ Found {len([n for n in all_news if n['symbol'] == symbol])} news items")
            else:
                print(f"   ✗ Failed to fetch: {response.status_code}")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    return all_news


def test_yahoo_finance_news(symbols: List[str]) -> List[Dict[str, Any]]:
    """Get real news from Yahoo Finance RSS feeds (free)."""
    print("\nTesting Yahoo Finance RSS feeds...")
    print("=" * 40)
    
    import feedparser
    all_news = []
    
    for symbol in symbols:
        print(f"\nFetching Yahoo Finance news for {symbol}...")
        
        try:
            # Yahoo Finance provides RSS feeds for each stock
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}"
            
            feed = feedparser.parse(rss_url)
            
            if feed.entries:
                for entry in feed.entries[:5]:  # Get top 5 news
                    news_item = {
                        'symbol': symbol,
                        'title': entry.title,
                        'summary': entry.get('summary', ''),
                        'url': entry.link,
                        'published': entry.get('published', ''),
                        'source': 'Yahoo Finance RSS',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }
                    all_news.append(news_item)
                    print(f"   • {news_item['title'][:80]}...")
                
                print(f"   ✓ Found {len(feed.entries)} news items")
            else:
                print(f"   ✗ No news found in RSS feed")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    return all_news


def test_google_news_rss(query: str) -> List[Dict[str, Any]]:
    """Get real news from Google News RSS (free)."""
    print(f"\nTesting Google News RSS for '{query}'...")
    print("=" * 40)
    
    import feedparser
    all_news = []
    
    try:
        # Google News RSS URL
        rss_url = f"https://news.google.com/rss/search?q={query}+stock+market&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            for entry in feed.entries[:10]:  # Get top 10 news
                news_item = {
                    'title': entry.title,
                    'url': entry.link,
                    'published': entry.get('published', ''),
                    'source': 'Google News',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'query': query
                }
                all_news.append(news_item)
                print(f"   • {news_item['title'][:80]}...")
            
            print(f"   ✓ Found {len(feed.entries)} news items")
        else:
            print(f"   ✗ No news found")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    return all_news


def test_newsapi_org():
    """Test NewsAPI.org (requires free API key)."""
    print("\nTesting NewsAPI.org...")
    print("=" * 40)
    
    # Check if API key exists
    api_key = os.getenv("NEWSAPI_KEY")
    
    if not api_key:
        print("   ℹ️  NewsAPI.org requires a free API key from https://newsapi.org")
        print("   ℹ️  Set NEWSAPI_KEY environment variable to use this source")
        return []
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'stock market',
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"   ✓ Found {len(articles)} articles")
            
            for article in articles[:5]:
                print(f"   • {article['title'][:80]}...")
            
            return articles
        else:
            print(f"   ✗ API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return []


def main():
    """Test various real news sources."""
    print("🔬 Real News API Testing")
    print("Testing multiple free news sources for stock market data")
    print()
    
    # Test stocks
    symbols = ["AAPL", "MSFT", "NVDA"]
    
    # Test different news sources
    all_news = []
    
    # 1. Yahoo Finance RSS (Most reliable free source)
    yahoo_news = test_yahoo_finance_news(symbols)
    all_news.extend(yahoo_news)
    
    # 2. Google News RSS
    google_news = test_google_news_rss("technology stocks")
    all_news.extend(google_news)
    
    # 3. FinViz (web scraping - use with caution)
    # Note: Uncomment to test, but be aware of rate limits
    # finviz_news = test_finviz_news(symbols)
    # all_news.extend(finviz_news)
    
    # 4. NewsAPI.org (if API key available)
    newsapi_articles = test_newsapi_org()
    
    # Save all news
    with open("real_news_test.json", "w") as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'yahoo_finance': yahoo_news,
            'google_news': google_news,
            'total_articles': len(all_news)
        }, f, indent=2)
    
    print(f"\n\n📊 Summary:")
    print(f"   Total news articles retrieved: {len(all_news)}")
    print(f"   - Yahoo Finance: {len(yahoo_news)} articles")
    print(f"   - Google News: {len(google_news)} articles")
    print(f"   - NewsAPI.org: {len(newsapi_articles) if newsapi_articles else 'Not tested'}")
    
    print("\n✅ Test completed!")
    print("📌 These are REAL news articles from actual news sources")
    print("📌 Yahoo Finance RSS is the most reliable free source for stock news")


if __name__ == "__main__":
    main()