#!/usr/bin/env python3
"""Run AIRAS-Trade pipeline with ONLY REAL DATA - No simulations or mocks."""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from airas.features.stock_research.retrieve.stock_news_subgraph import StockNewsSubgraph
from airas.features.stock_research.retrieve.investment_papers_subgraph import InvestmentPapersSubgraph
from airas.features.stock_research.create.create_investment_method_subgraph import CreateInvestmentMethodSubgraph
from airas.features.stock_research.create.experiment_planning_subgraph import ExperimentPlanningSubgraph
from airas.features.stock_research.create.local_execution_subgraph import LocalExecutionSubgraph
from airas.features.stock_research.create.results_analysis_subgraph import ResultsAnalysisSubgraph
from airas.features.stock_research.create.report_writer_subgraph import ReportWriterSubgraph


def run_real_data_pipeline():
    """Run the complete pipeline using ONLY real data."""
    print("=" * 80)
    print("🚀 AIRAS-Trade Pipeline - REAL DATA ONLY")
    print("=" * 80)
    print("This pipeline uses:")
    print("✅ REAL stock market data from Alpha Vantage API")
    print("✅ REAL news from Yahoo Finance RSS feeds")
    print("✅ REAL academic papers from ArXiv API")
    print("✅ REAL AI analysis from OpenAI API")
    print("❌ NO mock data, simulations, or dummy content")
    print("=" * 80)
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"stock_research_real_only_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initial state with real stock symbols
    initial_state = {
        "stock_symbols": ["AAPL", "NVDA", "MSFT"],  # Real stocks
        "time_period": "7d",
        "save_dir": output_dir,
        "use_real_data": True,
        "data_transparency": True
    }
    
    # Create tracking file
    tracking_file = os.path.join(output_dir, "data_sources_used.json")
    tracking_data = {
        "pipeline_start": datetime.now().isoformat(),
        "mode": "REAL DATA ONLY",
        "data_sources": []
    }
    
    try:
        # 1. Stock News Retrieval (REAL)
        print("\n" + "=" * 60)
        print("📰 Step 1: Retrieving REAL Stock News")
        print("=" * 60)
        
        news_subgraph = StockNewsSubgraph()
        state = news_subgraph.run(initial_state)
        
        tracking_data["data_sources"].append({
            "step": "Stock News",
            "source": "Yahoo Finance RSS",
            "type": "REAL",
            "articles_retrieved": len(state.get("raw_news", [])),
            "timestamp": datetime.now().isoformat()
        })
        
        # 2. Investment Papers Retrieval (REAL)
        print("\n" + "=" * 60)
        print("📚 Step 2: Retrieving REAL Academic Papers")
        print("=" * 60)
        
        papers_subgraph = InvestmentPapersSubgraph()
        state = papers_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Academic Papers",
            "source": "ArXiv API",
            "type": "REAL",
            "papers_retrieved": len(state.get("raw_papers", [])),
            "timestamp": datetime.now().isoformat()
        })
        
        # 3. Create Investment Method (REAL AI)
        print("\n" + "=" * 60)
        print("🤖 Step 3: Creating Investment Method with REAL AI")
        print("=" * 60)
        
        method_subgraph = CreateInvestmentMethodSubgraph()
        state = method_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Investment Method Creation",
            "source": "OpenAI API",
            "type": "REAL AI",
            "model": state.get("llm_name", "gpt-4o-mini"),
            "timestamp": datetime.now().isoformat()
        })
        
        # 4. Experiment Planning (REAL AI)
        print("\n" + "=" * 60)
        print("🔬 Step 4: Planning Experiments with REAL AI")
        print("=" * 60)
        
        experiment_subgraph = ExperimentPlanningSubgraph()
        state = experiment_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Experiment Planning",
            "source": "OpenAI API",
            "type": "REAL AI",
            "model": state.get("llm_name", "gpt-4o-mini"),
            "timestamp": datetime.now().isoformat()
        })
        
        # 5. Local Execution (Code generation only - no simulation)
        print("\n" + "=" * 60)
        print("💻 Step 5: Generating Executable Code (No Simulation)")
        print("=" * 60)
        
        execution_subgraph = LocalExecutionSubgraph()
        state["skip_execution"] = True  # Generate code but don't run it
        state = execution_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Code Generation",
            "source": "OpenAI API",
            "type": "REAL AI",
            "note": "Generated executable backtest code - ready for manual execution",
            "timestamp": datetime.now().isoformat()
        })
        
        # 6. Results Analysis (Based on strategy, not simulated results)
        print("\n" + "=" * 60)
        print("📊 Step 6: Analyzing Strategy (No Simulated Results)")
        print("=" * 60)
        
        # Create strategy analysis instead of result analysis
        state["experiment_results"] = [{
            "strategy_name": state.get("investment_method", {}).get("name", "Generated Strategy"),
            "type": "STRATEGY_ANALYSIS",
            "note": "This is a strategy analysis, not backtest results",
            "key_features": state.get("investment_method", {}).get("strategy_type", "Unknown"),
            "parameters": state.get("investment_method", {}).get("parameters", {}),
            "ready_for_execution": True
        }]
        
        analysis_subgraph = ResultsAnalysisSubgraph()
        state = analysis_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Strategy Analysis",
            "source": "OpenAI API",
            "type": "REAL AI",
            "note": "Analyzed strategy design, not backtest results",
            "timestamp": datetime.now().isoformat()
        })
        
        # 7. Report Writing (REAL AI)
        print("\n" + "=" * 60)
        print("📝 Step 7: Writing Report with REAL AI")
        print("=" * 60)
        
        report_subgraph = ReportWriterSubgraph()
        state = report_subgraph.run(state)
        
        tracking_data["data_sources"].append({
            "step": "Report Writing",
            "source": "OpenAI API",
            "type": "REAL AI",
            "model": state.get("llm_name", "gpt-4o-mini"),
            "timestamp": datetime.now().isoformat()
        })
        
        # Save tracking data
        tracking_data["pipeline_end"] = datetime.now().isoformat()
        with open(tracking_file, "w") as f:
            json.dump(tracking_data, f, indent=2)
        
        # Create summary
        print("\n" + "=" * 80)
        print("✅ PIPELINE COMPLETED - REAL DATA ONLY")
        print("=" * 80)
        print(f"\n📁 Output Directory: {output_dir}")
        print("\n📊 Data Sources Used:")
        for source in tracking_data["data_sources"]:
            print(f"   • {source['step']}: {source['source']} ({source['type']})")
        
        print("\n📌 Key Files Generated:")
        files = os.listdir(output_dir)
        for file in sorted(files):
            print(f"   • {file}")
        
        print("\n⚠️  IMPORTANT NOTES:")
        print("   1. All data is REAL - no simulations or mocks")
        print("   2. Backtest code was generated but NOT executed")
        print("   3. To run backtests, execute the generated Python files manually")
        print("   4. All news, papers, and analysis are from real sources")
        
        print("\n🎯 Next Steps:")
        print("   1. Review the generated strategy in 'investment_method.json'")
        print("   2. Examine the backtest code in the output directory")
        print("   3. Run the backtest manually if desired")
        print("   4. Read the final report for insights")
        
        return state
        
    except Exception as e:
        print(f"\n❌ Error in pipeline: {e}")
        tracking_data["error"] = str(e)
        tracking_data["pipeline_end"] = datetime.now().isoformat()
        with open(tracking_file, "w") as f:
            json.dump(tracking_data, f, indent=2)
        raise


if __name__ == "__main__":
    print("Starting AIRAS-Trade with REAL DATA ONLY...")
    print("This may take a few minutes as we fetch real data from APIs...")
    
    try:
        final_state = run_real_data_pipeline()
        print("\n✅ Pipeline completed successfully!")
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)