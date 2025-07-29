# Experiment Planning Subgraph

This subgraph designs backtesting experiments for the generated investment strategies.

## Components

### Nodes
1. **plan_experiments** - Defines test scenarios
2. **design_backtest** - Sets up time periods and data splits  
3. **set_parameters** - Configures risk limits and position sizes

### Data Flow
```
START → plan_experiments → design_backtest → set_parameters → END
```

### Input
- `investment_method`: The trading strategy to test
- `stock_symbols`: Stocks to include in backtest

### Output
- `experiment_plan`: Complete backtest configuration:
  - Time periods (train/test splits)
  - Performance metrics to track
  - Risk parameters
  - Position sizing rules
  - Data requirements

### Key Features
- Designs walk-forward analysis
- Sets up out-of-sample testing
- Defines performance benchmarks
- Configures risk limits

### Example Plan
- Training period: 2020-2022
- Testing period: 2023-2024
- Metrics: Sharpe ratio, max drawdown, returns
- Risk limit: 2% per trade