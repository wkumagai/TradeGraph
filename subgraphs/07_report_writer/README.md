# Report Writer Subgraph

This subgraph generates comprehensive investment research reports.

## Components

### Nodes
1. **compile_results** - Gathers all results
2. **generate_insights** - Creates AI insights
3. **create_report** - Produces final report

### Data Flow
```
START → compile_results → generate_insights → create_report → END
```

### Input
- All data from previous subgraphs:
  - Stock news and papers
  - Investment strategy
  - Backtest results
  - Analysis outcomes

### Output
- `final_report`: Multi-format report including:
  - Executive summary
  - Market analysis
  - Strategy description
  - Backtest results
  - Performance charts
  - Risk assessment
  - Recommendations

### Report Formats
- **Markdown**: Human-readable report
- **JSON**: Structured data
- **HTML**: Web-viewable (planned)
- **PDF**: Professional document (planned)

### Data Sources
- OpenAI API for insight generation

### Report Sections
1. Executive Summary
2. Market Context (news + papers)
3. Strategy Details
4. Backtest Results
5. Risk Analysis
6. Conclusions & Next Steps