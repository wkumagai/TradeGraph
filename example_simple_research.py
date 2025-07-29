#!/usr/bin/env python3
"""Simple example of using AIRAS-Trade for stock investment research.

This example shows how to research a single stock with minimal configuration.
"""

import os
from dotenv import load_dotenv
from src.airas.features.stock_research import (
    StockNewsSubgraph,
    CreateInvestmentMethodSubgraph
)

# Load environment variables
load_dotenv()

def simple_stock_research(symbol: str = "AAPL"):
    """Run a simple stock research analysis.
    
    Args:
        symbol: Stock symbol to research
    """
    print(f"🔍 Researching {symbol}...")
    
    # Initialize state
    state = {
        "stock_symbols": [symbol],
        "save_dir": f"./quick_research_{symbol}",
        "llm_name": "gpt-4o-mini-2024-07-18"
    }
    
    # Step 1: Get latest news
    print("\n📰 Retrieving latest news...")
    news_subgraph = StockNewsSubgraph()
    state = news_subgraph.run(state)
    
    print(f"Found {len(state.get('filtered_news', []))} relevant news articles")
    print("\nNews Summary Preview:")
    print(state.get('news_summary', 'No summary')[:500] + "...")
    
    # Step 2: Create investment idea
    print("\n💡 Generating investment strategy...")
    state["market_insights"] = state.get("news_summary", "")
    state["research_papers"] = "Recent momentum and value factor research"
    
    method_subgraph = CreateInvestmentMethodSubgraph()
    state = method_subgraph.run(state)
    
    # Display results
    method = state.get('investment_method', {})
    anomaly = state.get('market_anomaly', {})
    
    print(f"\n✨ Investment Method: {method.get('method_name', 'Unknown')}")
    print(f"📊 Market Anomaly: {anomaly.get('anomaly_name', 'Unknown')}")
    print(f"🎯 Type: {anomaly.get('anomaly_type', 'Unknown')}")
    
    print("\n📁 Full results saved to:", state.get('save_dir'))
    
    return state


if __name__ == "__main__":
    # Example: Research Apple stock
    simple_stock_research("AAPL")
    
    # You can also research other stocks:
    # simple_stock_research("TSLA")
    # simple_stock_research("NVDA")