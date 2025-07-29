#!/usr/bin/env python3
"""Complete Stock Investment Research Pipeline using AIRAS-Trade.

This script orchestrates all subgraphs to conduct comprehensive investment research.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all subgraphs
from src.airas.features.stock_research import (
    StockNewsSubgraph,
    InvestmentPapersSubgraph,
    CreateInvestmentMethodSubgraph,
    ExperimentPlanningSubgraph,
    LocalExecutionSubgraph,
    ResultsAnalysisSubgraph,
    ReportWriterSubgraph
)


def run_complete_stock_research_pipeline(
    stock_symbols: list,
    research_topic: str = "quantitative trading strategies",
    output_dir: str = None,
    llm_name: str = "gpt-4o-mini-2024-07-18"
):
    """Run the complete stock investment research pipeline.
    
    Args:
        stock_symbols: List of stock symbols to research (e.g., ["AAPL", "GOOGL"])
        research_topic: Investment research focus area
        output_dir: Directory to save all outputs
        llm_name: LLM model to use
    
    Returns:
        Dictionary with all research outputs
    """
    # Setup output directory
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"./stock_research_output_{timestamp}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize state
    state = {
        "stock_symbols": stock_symbols,
        "research_topic": research_topic,
        "save_dir": output_dir,
        "llm_name": llm_name,
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    print(f"Starting Stock Investment Research Pipeline")
    print(f"Stocks: {', '.join(stock_symbols)}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    
    try:
        # Phase 1: Research and Information Gathering
        print("\n📚 PHASE 1: Market Research and Information Gathering")
        print("-" * 60)
        
        # 1.1 Retrieve stock news
        print("\n1.1 Retrieving stock market news...")
        news_subgraph = StockNewsSubgraph(llm_name=llm_name)
        state = news_subgraph.run(state)
        print(f"✓ Retrieved {len(state.get('filtered_news', []))} relevant news articles")
        
        # 1.2 Retrieve investment research papers
        print("\n1.2 Searching for investment research papers...")
        papers_subgraph = InvestmentPapersSubgraph(llm_name=llm_name)
        state = papers_subgraph.run(state)
        print(f"✓ Found {len(state.get('paper_titles', []))} relevant research papers")
        
        # Phase 2: Investment Method Creation
        print("\n\n🧪 PHASE 2: Investment Method Development")
        print("-" * 60)
        
        print("\n2.1 Creating novel investment method...")
        method_subgraph = CreateInvestmentMethodSubgraph(llm_name=llm_name)
        
        # Add research insights to state
        state["market_insights"] = state.get("news_summary", "")
        state["research_papers"] = json.dumps(state.get("paper_summaries", [])[:5])
        
        state = method_subgraph.run(state)
        print(f"✓ Created investment method: {state.get('investment_method', {}).get('method_name', 'Unknown')}")
        print(f"✓ Identified anomaly: {state.get('market_anomaly', {}).get('anomaly_name', 'Unknown')}")
        
        # Phase 3: Experiment Planning and Execution
        print("\n\n🔬 PHASE 3: Strategy Testing and Backtesting")
        print("-" * 60)
        
        # 3.1 Plan experiments
        print("\n3.1 Planning backtest experiments...")
        planning_subgraph = ExperimentPlanningSubgraph(llm_name=llm_name)
        state = planning_subgraph.run(state)
        print(f"✓ Designed experiment: {state.get('experiment_design', {}).get('experiment_name', 'Unknown')}")
        
        # 3.2 Execute locally
        print("\n3.2 Executing backtest locally...")
        execution_subgraph = LocalExecutionSubgraph(llm_name=llm_name)
        state = execution_subgraph.run(state)
        
        if state.get("execution_status") == "success":
            print(f"✓ Backtest completed successfully")
            print(f"  - Metrics calculated: {len(state.get('performance_metrics', {}))}")
        else:
            print(f"⚠️ Backtest encountered errors")
            print(f"  - Check error logs in {output_dir}/execution/")
        
        # Phase 4: Analysis and Evaluation
        print("\n\n📊 PHASE 4: Results Analysis and Evaluation")
        print("-" * 60)
        
        print("\n4.1 Analyzing backtest results...")
        analysis_subgraph = ResultsAnalysisSubgraph(llm_name=llm_name)
        state = analysis_subgraph.run(state)
        
        eval_result = state.get('strategy_evaluation', {})
        print(f"✓ Strategy evaluation: {eval_result.get('viability_assessment', {}).get('overall_viability', 'Unknown')}")
        print(f"✓ Recommendation: {eval_result.get('recommendation', {}).get('action', 'Unknown')}")
        print(f"✓ Generated {len(state.get('key_insights', []))} key insights")
        
        # Phase 5: Report Generation
        print("\n\n📝 PHASE 5: Report Generation")
        print("-" * 60)
        
        print("\n5.1 Writing comprehensive research report...")
        report_subgraph = ReportWriterSubgraph(llm_name=llm_name)
        state = report_subgraph.run(state)
        print(f"✓ Generated investment research report")
        print(f"✓ Created HTML version for web viewing")
        
        # Summary
        print("\n\n" + "=" * 60)
        print("✅ RESEARCH PIPELINE COMPLETED")
        print("=" * 60)
        
        # Print key results
        metrics = state.get('performance_metrics', {})
        print(f"\n📈 Key Performance Metrics:")
        print(f"  - Total Return: {metrics.get('total_return', 'N/A')}")
        print(f"  - Sharpe Ratio: {metrics.get('sharpe_ratio', 'N/A')}")
        print(f"  - Max Drawdown: {metrics.get('max_drawdown', 'N/A')}")
        print(f"  - Win Rate: {metrics.get('win_rate', 'N/A')}")
        
        print(f"\n📁 All results saved to: {output_dir}")
        print(f"  - Full report: {output_dir}/report/investment_research_report.md")
        print(f"  - HTML report: {output_dir}/report/investment_research_report.html")
        print(f"  - Summary: {output_dir}/report/summary_report.md")
        
        # Save final state
        with open(os.path.join(output_dir, "final_state.json"), "w") as f:
            # Remove large text fields for cleaner state file
            state_to_save = {k: v for k, v in state.items() 
                           if k not in ['final_report', 'html_report', 'backtest_code']}
            json.dump(state_to_save, f, indent=2)
        
        return state
        
    except Exception as e:
        print(f"\n❌ ERROR: Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error state
        state["pipeline_error"] = str(e)
        state["pipeline_status"] = "failed"
        
        with open(os.path.join(output_dir, "error_state.json"), "w") as f:
            json.dump(state, f, indent=2)
        
        return state


def main():
    """Main function to run the pipeline with example parameters."""
    # Example usage
    stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]  # Top tech stocks
    
    # You can customize these parameters
    research_topic = "momentum and mean reversion strategies in tech stocks"
    
    # Run the pipeline
    results = run_complete_stock_research_pipeline(
        stock_symbols=stock_symbols,
        research_topic=research_topic,
        llm_name="gpt-4o-mini-2024-07-18"  # Use "gpt-4" for better quality
    )
    
    # Check final recommendation
    recommendation = results.get('strategy_evaluation', {}).get('recommendation', {}).get('action', 'Unknown')
    print(f"\n\n🎯 FINAL RECOMMENDATION: {recommendation}")


if __name__ == "__main__":
    main()