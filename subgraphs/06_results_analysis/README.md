# Results Analysis Subgraph

This subgraph analyzes backtest results and identifies patterns.

## Components

### Nodes
1. **analyze_performance** - Evaluates strategy performance
2. **calculate_metrics** - Computes key metrics
3. **identify_patterns** - Finds success/failure patterns

### Data Flow
```
START → analyze_performance → calculate_metrics → identify_patterns → END
```

### Input
- `backtest_results`: Output from execution
- `experiment_plan`: Original test configuration
- All data from shared state

### Output
- `analysis_results`: Comprehensive analysis including:
  - Performance metrics
  - Risk statistics  
  - Pattern identification
  - Success factors
  - Improvement suggestions

### Metrics Calculated
- **Returns**: Total, annualized, monthly
- **Risk**: Sharpe ratio, Sortino, max drawdown
- **Trading**: Win rate, profit factor
- **Statistical**: Alpha, beta, correlation

### Pattern Analysis
- Identifies market conditions for success
- Finds optimal parameter ranges
- Detects overfitting risks
- Suggests improvements