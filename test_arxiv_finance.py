#!/usr/bin/env python3
"""Test ArXiv API with finance-specific searches."""

import os
import sys
import json
import feedparser
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.airas.services.api_client.arxiv_client import ArxivClient


def test_finance_papers():
    """Test ArXiv with more specific finance queries."""
    print("Testing ArXiv API with finance-specific searches...")
    print("=" * 60)
    
    client = ArxivClient()
    
    # More specific finance queries
    queries = [
        # Quantitative finance specific
        "stock price prediction machine learning",
        "portfolio optimization reinforcement learning",
        "algorithmic trading deep learning",
        "financial time series forecasting",
        "market microstructure",
        
        # ArXiv category searches
        "cat:q-fin.TR",  # Trading and Market Microstructure
        "cat:q-fin.PM",  # Portfolio Management
        "cat:q-fin.ST",  # Statistical Finance
        "cat:q-fin.CP",  # Computational Finance
        
        # Combined searches
        "neural network AND stock market",
        "LSTM price prediction",
        "sentiment analysis trading"
    ]
    
    all_papers = []
    finance_papers = []
    
    for query in queries:
        print(f"\nSearching: '{query}'")
        print("-" * 40)
        
        try:
            xml_response = client.search_papers(
                query=query,
                max_results=5,
                sort_by="relevance",
                sort_order="descending"
            )
            
            feed = feedparser.parse(xml_response)
            print(f"Found {len(feed.entries)} papers")
            
            for entry in feed.entries:
                paper = {
                    "title": entry.title.replace("\n", " ").strip(),
                    "authors": [author.name for author in entry.authors],
                    "published": entry.published,
                    "arxiv_id": entry.id.split("/abs/")[-1],
                    "summary": entry.summary.replace("\n", " ").strip(),
                    "categories": [tag.term for tag in entry.tags],
                    "query": query
                }
                
                all_papers.append(paper)
                
                # Check if it's finance related
                finance_keywords = ["stock", "trading", "portfolio", "finance", "market", "investment", 
                                  "price", "return", "asset", "option", "derivative", "risk"]
                
                title_lower = paper["title"].lower()
                summary_lower = paper["summary"].lower()
                
                is_finance = any(keyword in title_lower or keyword in summary_lower 
                               for keyword in finance_keywords)
                
                # Check categories
                finance_categories = ["q-fin", "econ", "stat.ML", "cs.CE"]
                has_finance_cat = any(any(cat.startswith(fc) for fc in finance_categories) 
                                    for cat in paper["categories"])
                
                if is_finance or has_finance_cat:
                    finance_papers.append(paper)
                    print(f"   📈 {paper['title'][:80]}...")
                    print(f"      Categories: {', '.join(paper['categories'][:3])}")
                    print(f"      Date: {paper['published'][:10]}")
                else:
                    print(f"   • {paper['title'][:80]}...")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    # Save results
    with open("arxiv_finance_papers.json", "w") as f:
        json.dump(finance_papers, f, indent=2)
    
    print(f"\n\n📊 Summary:")
    print(f"   Total papers found: {len(all_papers)}")
    print(f"   Finance-related papers: {len(finance_papers)}")
    
    if finance_papers:
        print("\n📈 Sample Finance Papers:")
        for i, paper in enumerate(finance_papers[:5], 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'][:2])}")
            if len(paper['authors']) > 2:
                print(f"            + {len(paper['authors']) - 2} more")
            print(f"   Summary: {paper['summary'][:150]}...")
    
    return finance_papers


if __name__ == "__main__":
    papers = test_finance_papers()
    
    print("\n✅ Test completed!")
    print(f"📌 Found {len(papers)} finance-related papers from ArXiv")
    print("📌 These are REAL academic papers, not simulated data")