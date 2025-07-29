# TradeGraph

TradeGraph is a stock investment research pipeline built with LangGraph that uses real data sources to analyze markets, generate trading strategies, and produce comprehensive investment reports.

## Features

- **Real Data Integration**: 
  - ArXiv API for academic papers
  - Alpha Vantage for stock prices
  - Yahoo Finance RSS for news (needs fix)
  - OpenAI API for AI analysis

- **Modular Architecture**: 
  - 7 specialized subgraphs
  - State-based workflow management
  - Error resilient design

- **Automated Pipeline**:
  - Paper and news retrieval
  - Strategy generation
  - Backtest code creation
  - Performance analysis
  - Report generation

## Quick Start

### Prerequisites

```bash
# Required API Keys (add to .env file)
ALPHAVANTAGE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Installation

```bash
# Clone the repository
git clone https://github.com/wkumagai/TradeGraph.git
cd TradeGraph

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
# Test with real data
python test_pipeline_simple.py

# Run full pipeline
python run_pipeline.py
```

## Architecture

TradeGraph uses a hierarchical graph structure:

### Main Pipeline
- `StockNewsSubgraph` - Retrieves market news
- `InvestmentPapersSubgraph` - Fetches academic research
- `CreateInvestmentMethodSubgraph` - Generates trading strategies
- `ExperimentPlanningSubgraph` - Plans backtests
- `LocalExecutionSubgraph` - Creates executable code
- `ResultsAnalysisSubgraph` - Analyzes performance
- `ReportWriterSubgraph` - Generates reports

### Data Flow
1. **Retrieve** real market data and research
2. **Create** investment strategies using AI
3. **Execute** backtests (or generate code)
4. **Analyze** results and patterns
5. **Report** findings and insights

## Real Data Sources

| Source | Status | Usage |
|--------|--------|-------|
| Alpha Vantage | ✅ Working | Stock prices |
| ArXiv API | ✅ Working | Academic papers |
| Yahoo Finance | ❌ 404 Error | News (needs alternative) |
| OpenAI API | ✅ Working | AI analysis |

## Example Output

```json
{
  "papers": 6,          // Real ArXiv papers
  "stocks": 3,          // Real stock prices
  "strategy": "AI generated trading method",
  "backtest_code": "executable Python script"
}
```

## Project Structure

```
TradeGraph/
├── src/
│   └── tradegraph/
│       ├── core/           # Base classes
│       ├── features/       # Subgraph implementations
│       ├── services/       # API clients
│       └── types/          # Data types
├── tests/                  # Test files
├── examples/              # Usage examples
└── docs/                  # Documentation
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with LangGraph
- Inspired by AI research automation
- Uses real financial data sources