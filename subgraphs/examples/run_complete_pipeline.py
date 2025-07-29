#!/usr/bin/env python3
"""Example of running the complete TradeGraph pipeline."""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.tradegraph.features.stock_research import (
    StockNewsSubgraph,
    InvestmentPapersSubgraph,
    CreateInvestmentMethodSubgraph,
    ExperimentPlanningSubgraph,
    LocalExecutionSubgraph,
    ResultsAnalysisSubgraph,
    ReportWriterSubgraph
)


def run_pipeline(stock_symbols, execute_backtest=False):
    """Run the complete investment research pipeline."""
    print("🚀 Starting TradeGraph Pipeline")
    print(f"📊 Analyzing: {', '.join(stock_symbols)}")
    print("=" * 60)
    
    # Initialize shared state
    state = {
        "stock_symbols": stock_symbols,
        "raw_news": [],
        "filtered_news": [],
        "news_summary": "",
        "papers": [],
        "investment_method": {},
        "experiment_plan": {},
        "generated_code": "",
        "backtest_results": {},
        "analysis_results": {},
        "final_report": ""
    }
    
    # Pipeline stages
    stages = [
        ("📰 Stock News", StockNewsSubgraph()),
        ("📚 Investment Papers", InvestmentPapersSubgraph()),
        ("💡 Create Method", CreateInvestmentMethodSubgraph()),
        ("🧪 Plan Experiment", ExperimentPlanningSubgraph()),
        ("💻 Generate Code", LocalExecutionSubgraph()),
        ("📊 Analyze Results", ResultsAnalysisSubgraph()),
        ("📝 Write Report", ReportWriterSubgraph())
    ]
    
    # Run each stage
    for stage_name, subgraph in stages:
        print(f"\n{stage_name}...")
        try:
            # Special handling for local execution
            if "Generate Code" in stage_name:
                state["execute_locally"] = execute_backtest
            
            # Run subgraph
            result = subgraph.run(state)
            
            # Update state with results
            state.update(result)
            
            print(f"✅ {stage_name} completed")
            
        except Exception as e:
            print(f"❌ {stage_name} failed: {e}")
            # Continue with pipeline even if one stage fails
    
    # Save final results
    output_dir = f"pipeline_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save state
    with open(f"{output_dir}/state.json", 'w') as f:
        json.dump(state, f, indent=2)
    
    # Save report
    if state.get("final_report"):
        with open(f"{output_dir}/report.md", 'w') as f:
            f.write(state["final_report"])
    
    # Save generated code
    if state.get("generated_code"):
        with open(f"{output_dir}/backtest_code.py", 'w') as f:
            f.write(state["generated_code"])
    
    print(f"\n✨ Pipeline complete! Results saved to: {output_dir}/")
    return state


def main():
    """Run example pipeline."""
    # Configuration
    stocks = ["AAPL", "GOOGL", "MSFT"]
    execute = False  # Set to True to actually run backtests
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. AI features will fail.")
    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        print("⚠️  Warning: ALPHAVANTAGE_API_KEY not set. Stock data may be limited.")
    
    # Run pipeline
    results = run_pipeline(stocks, execute)
    
    # Show summary
    print("\n📊 Pipeline Summary:")
    print(f"- Papers found: {len(results.get('papers', []))}")
    print(f"- News items: {len(results.get('raw_news', []))}")
    print(f"- Strategy created: {'✅' if results.get('investment_method') else '❌'}")
    print(f"- Code generated: {'✅' if results.get('generated_code') else '❌'}")
    print(f"- Report created: {'✅' if results.get('final_report') else '❌'}")


if __name__ == "__main__":
    main()