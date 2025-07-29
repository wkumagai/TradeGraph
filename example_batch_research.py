#!/usr/bin/env python3
"""Batch research example for multiple stocks or strategies.

This example shows how to research multiple investment strategies in parallel.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from run_stock_research_pipeline import run_complete_stock_research_pipeline

# Load environment variables
load_dotenv()


def batch_research_strategies():
    """Research multiple investment strategies for different stock groups."""
    
    # Define different research scenarios
    research_scenarios = [
        {
            "name": "Tech Giants Momentum",
            "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
            "topic": "momentum strategies in large cap tech stocks"
        },
        {
            "name": "AI and Semiconductor Plays",
            "stocks": ["NVDA", "AMD", "INTC", "AVGO", "QCOM"],
            "topic": "AI-driven growth and semiconductor cycle trading"
        },
        {
            "name": "Value in Financial Sector",
            "stocks": ["JPM", "BAC", "WFC", "GS", "MS"],
            "topic": "value investing in undervalued financial stocks"
        },
        {
            "name": "High Dividend Yield Strategy",
            "stocks": ["VZ", "T", "XOM", "CVX", "PFE"],
            "topic": "dividend capture and yield optimization strategies"
        }
    ]
    
    results_summary = []
    
    print("🚀 Starting Batch Investment Research")
    print("=" * 60)
    
    for i, scenario in enumerate(research_scenarios, 1):
        print(f"\n📊 Research {i}/{len(research_scenarios)}: {scenario['name']}")
        print("-" * 60)
        
        try:
            # Run research for this scenario
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"./batch_research/{scenario['name'].replace(' ', '_')}_{timestamp}"
            
            results = run_complete_stock_research_pipeline(
                stock_symbols=scenario['stocks'],
                research_topic=scenario['topic'],
                output_dir=output_dir,
                llm_name="gpt-4o-mini-2024-07-18"
            )
            
            # Extract key results
            summary = {
                "scenario": scenario['name'],
                "stocks": scenario['stocks'],
                "strategy": results.get('investment_method', {}).get('method_name', 'Unknown'),
                "anomaly": results.get('market_anomaly', {}).get('anomaly_name', 'Unknown'),
                "viability": results.get('strategy_evaluation', {}).get('viability_assessment', {}).get('overall_viability', 'Unknown'),
                "recommendation": results.get('strategy_evaluation', {}).get('recommendation', {}).get('action', 'Unknown'),
                "performance": {
                    "return": results.get('performance_metrics', {}).get('total_return', 'N/A'),
                    "sharpe": results.get('performance_metrics', {}).get('sharpe_ratio', 'N/A'),
                    "max_dd": results.get('performance_metrics', {}).get('max_drawdown', 'N/A')
                },
                "output_dir": output_dir
            }
            
            results_summary.append(summary)
            
            print(f"✅ Completed: {scenario['name']}")
            print(f"   Strategy: {summary['strategy']}")
            print(f"   Recommendation: {summary['recommendation']}")
            
        except Exception as e:
            print(f"❌ Failed: {scenario['name']} - Error: {e}")
            results_summary.append({
                "scenario": scenario['name'],
                "error": str(e)
            })
    
    # Save batch summary
    print("\n\n📋 BATCH RESEARCH SUMMARY")
    print("=" * 60)
    
    summary_dir = "./batch_research"
    os.makedirs(summary_dir, exist_ok=True)
    
    with open(os.path.join(summary_dir, "batch_summary.json"), "w") as f:
        json.dump(results_summary, f, indent=2)
    
    # Print summary table
    print("\n| Scenario | Strategy | Viability | Recommendation |")
    print("|----------|----------|-----------|----------------|")
    
    for result in results_summary:
        if "error" not in result:
            print(f"| {result['scenario'][:20]:20} | {result['strategy'][:30]:30} | {result['viability']:15} | {result['recommendation']:15} |")
    
    print(f"\n✅ Batch research completed. Results saved to: {summary_dir}")
    
    return results_summary


def compare_sector_strategies():
    """Compare different strategies across market sectors."""
    
    sectors = {
        "Technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "META"],
        "Healthcare": ["JNJ", "UNH", "PFE", "LLY", "CVS"],
        "Finance": ["JPM", "BAC", "BRK.B", "V", "MA"],
        "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
        "Consumer": ["AMZN", "TSLA", "HD", "MCD", "NKE"]
    }
    
    # Research each sector with the same strategy
    research_topic = "sector rotation and relative strength strategies"
    
    print("🔄 Comparing Sector Rotation Strategies")
    print("=" * 60)
    
    sector_results = {}
    
    for sector, stocks in sectors.items():
        print(f"\n📈 Analyzing {sector} sector...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
            output_dir = f"./sector_comparison/{sector}_{timestamp}"
            
            results = run_complete_stock_research_pipeline(
                stock_symbols=stocks[:5],  # Top 5 stocks per sector
                research_topic=research_topic,
                output_dir=output_dir,
                llm_name="gpt-4o-mini-2024-07-18"
            )
            
            sector_results[sector] = {
                "performance": results.get('performance_metrics', {}),
                "recommendation": results.get('strategy_evaluation', {}).get('recommendation', {}).get('action', 'Unknown')
            }
            
        except Exception as e:
            print(f"❌ Error analyzing {sector}: {e}")
            sector_results[sector] = {"error": str(e)}
    
    # Save sector comparison
    with open("./sector_comparison/comparison_results.json", "w") as f:
        json.dump(sector_results, f, indent=2)
    
    return sector_results


if __name__ == "__main__":
    # Example 1: Run batch research on different strategies
    print("Example 1: Batch Strategy Research\n")
    batch_results = batch_research_strategies()
    
    # Example 2: Compare sectors (uncomment to run)
    # print("\n\nExample 2: Sector Comparison\n")
    # sector_results = compare_sector_strategies()