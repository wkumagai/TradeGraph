# Local Execution Subgraph

This subgraph generates executable Python code for backtesting strategies.

## Components

### Nodes
1. **generate_code** - Creates Python backtest code
2. **prepare_environment** - Sets up dependencies
3. **run_backtest** - Executes the backtest (optional)

### Data Flow
```
START → generate_code → prepare_environment → Decision → run_backtest → END
                                                    ↓
                                                   END
```

### Input
- `investment_method`: Trading strategy
- `experiment_plan`: Backtest configuration
- `execute_locally`: Boolean flag for execution

### Output
- `generated_code`: Complete Python script including:
  - Data fetching (yfinance)
  - Strategy implementation
  - Performance calculation
  - Results visualization
  - Saved as `backtest_code.py`

### Code Features
- Uses pandas, numpy, yfinance
- Implements the exact strategy
- Calculates Sharpe ratio, returns, drawdown
- Generates performance plots
- Saves results to JSON

### Execution Mode
- If `execute_locally=True`: Runs the backtest
- If `execute_locally=False`: Only generates code