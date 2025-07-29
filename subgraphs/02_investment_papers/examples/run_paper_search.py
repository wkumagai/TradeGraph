#!/usr/bin/env python3
"""Example of running the Investment Papers Subgraph independently."""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.tradegraph.features.stock_research import InvestmentPapersSubgraph


def main():
    """Search and retrieve academic papers on algorithmic trading."""
    print("📚 Searching for investment research papers...")
    print("-" * 50)
    
    # Initialize subgraph
    papers_subgraph = InvestmentPapersSubgraph()
    
    # Run the subgraph
    try:
        result = papers_subgraph.run({
            "papers": []
        })
        
        # Display results
        print(f"\n📄 Found {len(result['papers'])} relevant papers:\n")
        
        for i, paper in enumerate(result['papers'], 1):
            print(f"{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'][:3])}")
            if len(paper['authors']) > 3:
                print(f"            ... and {len(paper['authors'])-3} more")
            print(f"   Date: {paper['published']}")
            print(f"   ArXiv ID: {paper['arxiv_id']}")
            print()
        
        # Save results
        output_file = f"papers_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Results saved to: {output_file}")
        
        # Show summary
        print("\n📊 Summary:")
        print(f"- Total papers: {len(result['papers'])}")
        categories = {}
        for paper in result['papers']:
            for cat in paper.get('categories', []):
                categories[cat] = categories.get(cat, 0) + 1
        print("- Categories:", ', '.join(f"{k}({v})" for k, v in categories.items()))
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()