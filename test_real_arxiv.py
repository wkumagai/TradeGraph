#!/usr/bin/env python3
"""Test ArXiv API with real paper retrieval."""

import os
import sys
import json
import feedparser
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.airas.services.api_client.arxiv_client import ArxivClient


def test_arxiv_real_papers():
    """Test real ArXiv paper retrieval."""
    print("Testing ArXiv API with real paper search...")
    print("=" * 60)
    
    # Initialize ArXiv client
    client = ArxivClient()
    
    # Test queries related to quantitative finance and trading
    queries = [
        "momentum trading strategy",
        "mean reversion stock market", 
        "machine learning trading",
        "quantitative finance portfolio optimization",
        "high frequency trading"
    ]
    
    all_papers = []
    
    for query in queries:
        print(f"\nSearching ArXiv for: '{query}'")
        print("-" * 40)
        
        try:
            # Search with ArXiv client
            xml_response = client.search_papers(
                query=query,
                max_results=3,
                sort_by="submittedDate",
                sort_order="descending"
            )
            
            # Parse XML response
            feed = feedparser.parse(xml_response)
            
            print(f"Found {len(feed.entries)} papers")
            
            for i, entry in enumerate(feed.entries, 1):
                paper = {
                    "title": entry.title,
                    "authors": [author.name for author in entry.authors],
                    "published": entry.published,
                    "updated": entry.updated,
                    "summary": entry.summary,
                    "arxiv_id": entry.id.split("/abs/")[-1],
                    "pdf_url": entry.id.replace("/abs/", "/pdf/") + ".pdf",
                    "categories": [tag.term for tag in entry.tags],
                    "query": query
                }
                
                all_papers.append(paper)
                
                # Display paper info
                print(f"\n{i}. {paper['title']}")
                print(f"   Authors: {', '.join(paper['authors'][:3])}")
                if len(paper['authors']) > 3:
                    print(f"            + {len(paper['authors']) - 3} more")
                print(f"   Published: {paper['published'][:10]}")
                print(f"   ArXiv ID: {paper['arxiv_id']}")
                print(f"   Categories: {', '.join(paper['categories'][:3])}")
                print(f"   Summary: {paper['summary'][:200]}...")
                
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
    
    # Save all papers
    output_file = "arxiv_real_papers.json"
    with open(output_file, "w") as f:
        json.dump(all_papers, f, indent=2)
    
    print(f"\n\n✅ Successfully retrieved {len(all_papers)} real papers from ArXiv")
    print(f"📁 Saved to: {output_file}")
    
    # Analyze categories
    categories = {}
    for paper in all_papers:
        for cat in paper['categories']:
            categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Paper Categories Distribution:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {cat}: {count} papers")
    
    return all_papers


def test_arxiv_by_category():
    """Test searching by specific ArXiv categories."""
    print("\n\nTesting ArXiv search by finance categories...")
    print("=" * 60)
    
    client = ArxivClient()
    
    # Quantitative Finance categories
    q_fin_categories = [
        "q-fin.ST",  # Statistical Finance
        "q-fin.PM",  # Portfolio Management
        "q-fin.TR",  # Trading and Market Microstructure
        "q-fin.CP",  # Computational Finance
        "q-fin.RM"   # Risk Management
    ]
    
    category_papers = []
    
    for category in q_fin_categories:
        print(f"\nSearching category: {category}")
        
        try:
            # Search by category
            xml_response = client.search_papers(
                query=f"cat:{category}",
                max_results=2,
                sort_by="submittedDate",
                sort_order="descending"
            )
            
            feed = feedparser.parse(xml_response)
            print(f"Found {len(feed.entries)} recent papers")
            
            for entry in feed.entries:
                print(f"   • {entry.title[:80]}...")
                print(f"     {entry.published[:10]}")
                category_papers.append({
                    "title": entry.title,
                    "category": category,
                    "date": entry.published
                })
                
        except Exception as e:
            print(f"Error searching category {category}: {e}")
    
    return category_papers


if __name__ == "__main__":
    print("🔬 ArXiv API Real Paper Retrieval Test")
    print("This test uses the actual ArXiv API to retrieve real academic papers")
    print()
    
    # Test general search
    papers = test_arxiv_real_papers()
    
    # Test category search
    category_papers = test_arxiv_by_category()
    
    print("\n\n✅ ArXiv API test completed!")
    print(f"📌 Retrieved {len(papers)} papers from keyword search")
    print(f"📌 Retrieved {len(category_papers)} papers from category search")
    print("\n⚠️  These are REAL academic papers from ArXiv, not simulated data")