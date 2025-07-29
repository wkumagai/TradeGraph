#!/usr/bin/env python3
"""Example of running the Stock News Subgraph independently."""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.tradegraph.features.stock_research import StockNewsSubgraph


def main():
    """Run stock news retrieval for given symbols."""
    # Define stocks to analyze
    stock_symbols = ["AAPL", "GOOGL", "MSFT"]
    
    print(f"🔍 Retrieving news for: {', '.join(stock_symbols)}")
    print("-" * 50)
    
    # Initialize subgraph
    news_subgraph = StockNewsSubgraph()
    
    # Run the subgraph
    try:
        result = news_subgraph.run({
            "stock_symbols": stock_symbols,
            "raw_news": [],
            "filtered_news": [],
            "news_summary": ""
        })
        
        # Display results
        print(f"\n📰 Retrieved {len(result['raw_news'])} total news items")
        print(f"✅ Filtered to {len(result['filtered_news'])} relevant items")
        
        if result['news_summary']:
            print(f"\n📊 News Summary:\n{result['news_summary']}")
        
        # Save results
        output_file = f"news_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: Yahoo Finance RSS currently returns 404. Consider alternative news sources.")


if __name__ == "__main__":
    main()