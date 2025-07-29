# Create Investment Method Subgraph

This subgraph generates investment strategies based on analyzed news and academic papers.

## Components

### Nodes
1. **analyze_context** - Analyzes news and papers for insights
2. **generate_strategy** - Uses AI to create trading strategy
3. **validate_method** - Validates strategy consistency

### Data Flow
```
START → analyze_context → generate_strategy → validate_method → END
```

### Input
- `filtered_news`: Relevant market news
- `papers`: Academic papers with methods
- `stock_symbols`: Target stocks

### Output
- `investment_method`: Complete trading strategy including:
  - Strategy name
  - Description
  - Entry/exit conditions
  - Risk management rules
  - Position sizing
  - Implementation steps

### Data Sources
- OpenAI API (GPT-4) - ✅ Working

### Example Strategy Output
Generates strategies like:
- Momentum-based trading
- Mean reversion strategies
- ML-enhanced portfolio optimization
- Risk parity approaches