"""Node for creating executable backtest code."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def create_backtest_code_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create executable Python code for backtesting the trading strategy.
    
    This node generates complete, runnable backtesting code based on
    the strategy, data requirements, and metrics.
    """
    trading_strategy = state.get("trading_strategy", {})
    dataset_specification = state.get("dataset_specification", {})
    evaluation_metrics = state.get("evaluation_metrics", {})
    experiment_design = state.get("experiment_design", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Create complete, executable Python code for backtesting this trading strategy.

Trading Strategy:
{json.dumps(trading_strategy, indent=2)}

Dataset Specification:
{json.dumps(dataset_specification, indent=2)}

Evaluation Metrics:
{json.dumps(evaluation_metrics, indent=2)}

Experiment Design:
{json.dumps(experiment_design, indent=2)}

Generate a complete Python script with:

1. All necessary imports
2. Data download and preprocessing
3. Strategy implementation
4. Backtesting engine
5. Metric calculations
6. Result visualization
7. Report generation

The code should be production-ready with error handling and logging.

Structure the code as follows:

```python
#!/usr/bin/env python3
\"\"\"
Trading Strategy Backtest
Strategy: [Name]
Description: [Brief description]
\"\"\"

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {{
    'start_date': 'YYYY-MM-DD',
    'end_date': 'YYYY-MM-DD',
    'initial_capital': 100000,
    'commission': 0.001,  # 0.1%
    # Add strategy-specific parameters
}}

class DataLoader:
    \"\"\"Handle data downloading and preprocessing.\"\"\"
    
    def __init__(self, symbols, start_date, end_date):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
    
    def download_data(self):
        \"\"\"Download price data from Yahoo Finance.\"\"\"
        # Implementation
        pass
    
    def preprocess_data(self, data):
        \"\"\"Clean and prepare data for strategy.\"\"\"
        # Implementation
        pass

class TradingStrategy:
    \"\"\"Implement the trading strategy logic.\"\"\"
    
    def __init__(self, parameters):
        self.parameters = parameters
    
    def generate_signals(self, data):
        \"\"\"Generate trading signals based on strategy rules.\"\"\"
        # Implementation based on trading_strategy
        pass
    
    def calculate_positions(self, signals, data):
        \"\"\"Convert signals to position sizes.\"\"\"
        # Implementation
        pass

class Backtester:
    \"\"\"Run the backtest and calculate performance.\"\"\"
    
    def __init__(self, initial_capital, commission):
        self.initial_capital = initial_capital
        self.commission = commission
    
    def run_backtest(self, data, positions):
        \"\"\"Execute the backtest.\"\"\"
        # Implementation
        pass
    
    def calculate_metrics(self, returns, positions):
        \"\"\"Calculate all performance metrics.\"\"\"
        # Implementation based on evaluation_metrics
        pass

class ResultAnalyzer:
    \"\"\"Analyze and visualize backtest results.\"\"\"
    
    def __init__(self, results):
        self.results = results
    
    def create_visualizations(self):
        \"\"\"Generate all required plots.\"\"\"
        # Implementation
        pass
    
    def generate_report(self):
        \"\"\"Create comprehensive report.\"\"\"
        # Implementation
        pass

def main():
    \"\"\"Main execution function.\"\"\"
    logger.info("Starting backtest...")
    
    try:
        # 1. Load data
        data_loader = DataLoader(
            symbols=['SPY'],  # Adjust based on strategy
            start_date=CONFIG['start_date'],
            end_date=CONFIG['end_date']
        )
        data = data_loader.download_data()
        processed_data = data_loader.preprocess_data(data)
        
        # 2. Generate signals
        strategy = TradingStrategy(CONFIG)
        signals = strategy.generate_signals(processed_data)
        positions = strategy.calculate_positions(signals, processed_data)
        
        # 3. Run backtest
        backtester = Backtester(
            initial_capital=CONFIG['initial_capital'],
            commission=CONFIG['commission']
        )
        results = backtester.run_backtest(processed_data, positions)
        metrics = backtester.calculate_metrics(results['returns'], positions)
        
        # 4. Analyze results
        analyzer = ResultAnalyzer({{**results, **metrics}})
        analyzer.create_visualizations()
        report = analyzer.generate_report()
        
        # 5. Save results
        with open('backtest_results.json', 'w') as f:
            json.dump({{**metrics, 'config': CONFIG}}, f, indent=2)
        
        print(report)
        logger.info("Backtest completed successfully!")
        
    except Exception as e:
        logger.error(f"Backtest failed: {{e}}")
        raise

if __name__ == "__main__":
    main()
```

Make the code complete and executable with all logic implemented."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        backtest_code = content
        
        # Clean up the code if it has markdown backticks
        if "```python" in backtest_code:
            # Extract code between backticks
            start = backtest_code.find("```python") + 9
            end = backtest_code.rfind("```")
            if end > start:
                backtest_code = backtest_code[start:end].strip()
    except Exception as e:
        print(f"Error creating backtest code: {e}")
        backtest_code = f"# Error generating code: {e}"
    
    # Save backtest code
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "experiment", "backtest.py"), "w") as f:
        f.write(backtest_code)
    
    # Also create a requirements file
    requirements = """# Requirements for backtest
numpy>=1.21.0
pandas>=1.3.0
yfinance>=0.2.18
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
scikit-learn>=1.0.0
ta>=0.10.2  # Technical analysis library
quantstats>=0.0.59  # Performance analytics
"""
    
    with open(os.path.join(save_dir, "experiment", "requirements.txt"), "w") as f:
        f.write(requirements)
    
    # Update state
    state["backtest_code"] = backtest_code
    
    print("Backtest code generated")
    
    return state