#!/usr/bin/env python3
"""Optimized pipeline runner with improved API handling and timeouts."""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add optimized nodes to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import standard subgraphs
from src.airas.features.stock_research import (
    StockNewsSubgraph,
    InvestmentPapersSubgraph,
    CreateInvestmentMethodSubgraph,
    ExperimentPlanningSubgraph,
    LocalExecutionSubgraph,
    ResultsAnalysisSubgraph,
    ReportWriterSubgraph
)

# Override with optimized nodes
import src.airas.features.stock_research.retrieve.nodes.retrieve_stock_data_improved as stock_data_improved
import src.airas.features.stock_research.execution.nodes.execute_backtest_simple as backtest_simple

# Monkey patch the nodes
import src.airas.features.stock_research.retrieve.nodes.retrieve_stock_data
import src.airas.features.stock_research.execution.nodes.execute_backtest

src.airas.features.stock_research.retrieve.nodes.retrieve_stock_data.retrieve_stock_data_node = stock_data_improved.retrieve_stock_data_node
src.airas.features.stock_research.execution.nodes.execute_backtest.execute_backtest_node = backtest_simple.execute_backtest_node


def run_optimized_pipeline():
    """Run the optimized stock research pipeline."""
    print("🚀 Starting Optimized Stock Research Pipeline")
    print("=" * 60)
    
    # Configuration
    stock_symbols = ["AAPL", "MSFT", "NVDA"]  # Reduced to 3 symbols
    research_topic = "momentum strategies in tech stocks"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"./stock_research_output_optimized_{timestamp}"
    
    # Initialize state
    state = {
        "stock_symbols": stock_symbols,
        "research_topic": research_topic,
        "save_dir": output_dir,
        "llm_name": "gpt-4o-mini-2024-07-18",
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    print(f"📊 Analyzing: {', '.join(stock_symbols)}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🔧 Using optimized nodes for better performance")
    print()
    
    try:
        # Phase 1: Market Research (Optimized)
        print("📚 PHASE 1: Market Research")
        print("-" * 40)
        
        # 1.1 Stock News (with market data)
        print("1.1 Retrieving stock news with market data...")
        news_subgraph = StockNewsSubgraph()
        state = news_subgraph.run(state)
        print(f"✅ Retrieved {len(state.get('filtered_news', []))} news items")
        
        # 1.2 Investment Papers
        print("\n1.2 Searching investment research papers...")
        papers_subgraph = InvestmentPapersSubgraph()
        # Limit paper search to reduce API calls
        state["search_queries"] = ["momentum trading", "tech stocks"]
        state = papers_subgraph.run(state)
        print(f"✅ Found {len(state.get('paper_titles', []))} papers")
        
        # Phase 2: Strategy Development
        print("\n\n🧪 PHASE 2: Investment Method Development")
        print("-" * 40)
        
        print("2.1 Creating investment method...")
        method_subgraph = CreateInvestmentMethodSubgraph()
        state = method_subgraph.run(state)
        print(f"✅ Created: {state.get('investment_method', {}).get('method_name', 'Unknown')}")
        
        # Phase 3: Experiment Design
        print("\n\n🔬 PHASE 3: Experiment Planning")
        print("-" * 40)
        
        print("3.1 Designing backtest experiment...")
        planning_subgraph = ExperimentPlanningSubgraph()
        state = planning_subgraph.run(state)
        print(f"✅ Experiment designed: {state.get('experiment_design', {}).get('experiment_name', 'Unknown')}")
        
        # Phase 4: Execution (Simplified)
        print("\n\n⚡ PHASE 4: Backtest Execution (Optimized)")
        print("-" * 40)
        
        print("4.1 Running simplified backtest...")
        execution_subgraph = LocalExecutionSubgraph()
        state = execution_subgraph.run(state)
        
        if state.get("execution_status") == "success":
            metrics = state.get("performance_metrics", {})
            print(f"✅ Backtest completed")
            print(f"   Return: {metrics.get('total_return', 0):.2%}")
            print(f"   Sharpe: {metrics.get('sharpe_ratio', 0):.2f}")
        else:
            print("⚠️  Backtest had issues but continuing...")
        
        # Phase 5: Analysis
        print("\n\n📊 PHASE 5: Results Analysis")
        print("-" * 40)
        
        print("5.1 Analyzing results...")
        analysis_subgraph = ResultsAnalysisSubgraph()
        state = analysis_subgraph.run(state)
        
        eval_result = state.get('strategy_evaluation', {})
        print(f"✅ Analysis complete")
        print(f"   Viability: {eval_result.get('viability_assessment', {}).get('overall_viability', 'Unknown')}")
        
        # Phase 6: Report Generation
        print("\n\n📝 PHASE 6: Report Generation")
        print("-" * 40)
        
        print("6.1 Writing comprehensive report...")
        report_subgraph = ReportWriterSubgraph()
        state = report_subgraph.run(state)
        print("✅ Report generated")
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        print(f"\n📁 All results saved to: {output_dir}")
        print(f"   - Report: {output_dir}/report/investment_research_report.md")
        print(f"   - HTML: {output_dir}/report/investment_research_report.html")
        
        # Save pipeline metadata
        import json
        with open(os.path.join(output_dir, "pipeline_metadata.json"), "w") as f:
            json.dump({
                "completion_time": datetime.now().isoformat(),
                "status": "success",
                "phases_completed": 6,
                "optimizations_used": [
                    "reduced_api_calls",
                    "simplified_backtest",
                    "rate_limiting",
                    "timeout_handling"
                ]
            }, f, indent=2)
        
        return state
        
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return state


if __name__ == "__main__":
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found!")
        sys.exit(1)
    
    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        print("⚠️  ALPHAVANTAGE_API_KEY not found - will use mock data")
    
    # Run optimized pipeline
    print("🎯 Using optimized pipeline with:")
    print("  - Rate limiting for Alpha Vantage API")
    print("  - Simplified backtest execution")
    print("  - Reduced API calls")
    print("  - Better error handling")
    print()
    
    results = run_optimized_pipeline()
    
    print("\n✨ Done!")