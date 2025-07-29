"""Node for creating report visualizations."""

import os
import json
from typing import Dict, Any, List


def create_visualizations_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create visualization specifications for the report.
    
    This node defines charts and graphs to include in the report.
    Note: Actual chart generation would require matplotlib/plotly in execution.
    """
    performance_metrics = state.get("performance_metrics", {})
    
    # Define visualizations to create
    visualizations = []
    
    # 1. Cumulative Returns Chart
    visualizations.append({
        "type": "line_chart",
        "title": "Cumulative Returns vs Benchmark",
        "description": "Strategy performance over time compared to S&P 500",
        "data_required": ["daily_returns", "benchmark_returns"],
        "code": """
import matplotlib.pyplot as plt
import pandas as pd

# Plot cumulative returns
fig, ax = plt.subplots(figsize=(12, 6))
(1 + returns).cumprod().plot(ax=ax, label='Strategy')
(1 + benchmark_returns).cumprod().plot(ax=ax, label='S&P 500')
ax.set_title('Cumulative Returns vs Benchmark')
ax.set_xlabel('Date')
ax.set_ylabel('Cumulative Return')
ax.legend()
plt.savefig('cumulative_returns.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # 2. Drawdown Chart
    visualizations.append({
        "type": "area_chart",
        "title": "Strategy Drawdown",
        "description": "Underwater equity curve showing drawdowns",
        "data_required": ["cumulative_returns"],
        "code": """
# Calculate and plot drawdown
rolling_max = cumulative_returns.expanding().max()
drawdown = (cumulative_returns - rolling_max) / rolling_max

fig, ax = plt.subplots(figsize=(12, 4))
drawdown.plot(ax=ax, kind='area', color='red', alpha=0.3)
ax.set_title('Strategy Drawdown')
ax.set_xlabel('Date')
ax.set_ylabel('Drawdown %')
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.savefig('drawdown.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # 3. Monthly Returns Heatmap
    visualizations.append({
        "type": "heatmap",
        "title": "Monthly Returns Heatmap",
        "description": "Returns by month and year",
        "data_required": ["daily_returns"],
        "code": """
import seaborn as sns

# Create monthly returns matrix
monthly_returns = returns.resample('M').sum()
monthly_matrix = monthly_returns.pivot_table(
    values='returns',
    index=monthly_returns.index.month,
    columns=monthly_returns.index.year
)

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(monthly_matrix, annot=True, fmt='.2%', cmap='RdYlGn', center=0, ax=ax)
ax.set_title('Monthly Returns Heatmap')
ax.set_xlabel('Year')
ax.set_ylabel('Month')
plt.savefig('monthly_returns_heatmap.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # 4. Performance Metrics Bar Chart
    visualizations.append({
        "type": "bar_chart",
        "title": "Key Performance Metrics",
        "description": "Comparison of important metrics",
        "data_required": ["performance_metrics"],
        "code": f"""
# Plot key metrics
metrics = {{
    'Annual Return': {performance_metrics.get('total_return', 0)},
    'Sharpe Ratio': {performance_metrics.get('sharpe_ratio', 0)},
    'Max Drawdown': {performance_metrics.get('max_drawdown', 0)},
    'Win Rate': {performance_metrics.get('win_rate', 0)}
}}

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(metrics.keys(), metrics.values())
ax.set_title('Key Performance Metrics')
ax.set_ylabel('Value')
for i, (k, v) in enumerate(metrics.items()):
    ax.text(i, v, f'{{v:.2f}}', ha='center', va='bottom')
plt.savefig('performance_metrics.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # 5. Rolling Sharpe Ratio
    visualizations.append({
        "type": "line_chart",
        "title": "Rolling 6-Month Sharpe Ratio",
        "description": "Strategy consistency over time",
        "data_required": ["daily_returns"],
        "code": """
# Calculate rolling Sharpe ratio
rolling_sharpe = returns.rolling(126).mean() / returns.rolling(126).std() * np.sqrt(252)

fig, ax = plt.subplots(figsize=(12, 6))
rolling_sharpe.plot(ax=ax)
ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
ax.axhline(y=1, color='green', linestyle='--', alpha=0.5, label='Sharpe = 1')
ax.set_title('Rolling 6-Month Sharpe Ratio')
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
plt.savefig('rolling_sharpe.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # 6. Trade Distribution
    visualizations.append({
        "type": "histogram",
        "title": "Trade Returns Distribution",
        "description": "Distribution of individual trade returns",
        "data_required": ["trade_returns"],
        "code": """
# Plot trade returns distribution
fig, ax = plt.subplots(figsize=(10, 6))
trade_returns.hist(bins=50, ax=ax, alpha=0.7, color='blue')
ax.axvline(x=0, color='red', linestyle='--', label='Break-even')
ax.axvline(x=trade_returns.mean(), color='green', linestyle='--', label=f'Mean: {trade_returns.mean():.2%}')
ax.set_title('Trade Returns Distribution')
ax.set_xlabel('Return %')
ax.set_ylabel('Frequency')
ax.legend()
plt.savefig('trade_distribution.png', dpi=300, bbox_inches='tight')
"""
    })
    
    # Save visualization specifications
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "report", "visualizations.json"), "w") as f:
        json.dump(visualizations, f, indent=2)
    
    # Update state
    state["visualizations"] = visualizations
    
    print(f"Created {len(visualizations)} visualization specifications")
    
    return state