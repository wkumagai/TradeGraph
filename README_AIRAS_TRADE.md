# AIRAS-Trade: AI-Powered Stock Investment Research System

**AIRAS-Trade** is an autonomous AI system for stock investment research, adapted from the original [AIRAS](https://github.com/airas-org/airas) project. It automates the entire investment research process from market analysis to strategy backtesting and report generation.

## 🚀 Key Features

- **Market Intelligence**: Automated collection and analysis of stock news and research papers
- **Strategy Generation**: AI-driven creation of novel investment strategies and market anomaly detection
- **Backtesting**: Local execution of trading strategies with comprehensive performance analysis
- **Professional Reports**: Automated generation of investment research reports in Markdown and HTML

## 📊 System Architecture

```
AIRAS-Trade Pipeline:
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Market Research │ --> │ Strategy Creation│ --> │ Experiment Plan │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           |
                                                           v
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Report Writing  │ <-- │ Result Analysis  │ <-- │ Local Backtest  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.10 or 3.11 (NOT 3.13+)
- Git
- API keys for OpenAI (required), Anthropic (optional)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/airas-trade.git
cd airas-trade

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install AIRAS-Trade
pip install -e .

# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY="sk-proj-..."
ANTHROPIC_API_KEY="sk-ant-..."  # Optional
EOF
```

## 🚀 Quick Start

### Simple Stock Research

```python
from src.airas.features.stock_research import StockNewsSubgraph, CreateInvestmentMethodSubgraph

# Research a single stock
state = {
    "stock_symbols": ["AAPL"],
    "save_dir": "./aapl_research",
    "llm_name": "gpt-4o-mini-2024-07-18"
}

# Get news and create strategy
news_subgraph = StockNewsSubgraph()
state = news_subgraph.run(state)

method_subgraph = CreateInvestmentMethodSubgraph()
state = method_subgraph.run(state)

print(f"Strategy: {state['investment_method']['method_name']}")
```

### Complete Research Pipeline

```bash
# Run full pipeline for tech stocks
python run_stock_research_pipeline.py
```

This will:
1. Collect and analyze market news
2. Search for relevant research papers
3. Generate a novel investment strategy
4. Create and execute a backtest
5. Analyze results and generate insights
6. Produce a professional research report

## 📚 Core Components

### 1. Research & Information Gathering
- **StockNewsSubgraph**: Retrieves and analyzes stock market news
- **InvestmentPapersSubgraph**: Searches academic papers on investment strategies

### 2. Strategy Creation
- **CreateInvestmentMethodSubgraph**: Generates novel investment strategies
  - Identifies market anomalies
  - Designs trading rules
  - Defines risk management

### 3. Experiment Planning & Execution
- **ExperimentPlanningSubgraph**: Creates comprehensive backtest plans
- **LocalExecutionSubgraph**: Executes backtests locally with error handling

### 4. Analysis & Evaluation
- **ResultsAnalysisSubgraph**: Analyzes performance and generates insights
  - Performance metrics calculation
  - Strategy viability assessment
  - Risk analysis

### 5. Report Generation
- **ReportWriterSubgraph**: Creates professional investment research reports
  - Markdown and HTML output
  - Visualizations and charts
  - Executive summaries

## 🎯 Usage Examples

### Example 1: Research Multiple Strategies

```python
# See example_batch_research.py
python example_batch_research.py
```

This researches different strategies:
- Tech Giants Momentum
- AI and Semiconductor Plays
- Value in Financial Sector
- High Dividend Yield Strategy

### Example 2: Simple Research

```python
# See example_simple_research.py
python example_simple_research.py
```

Quick research on a single stock with minimal configuration.

## 📈 Output Structure

```
stock_research_output/
├── news_summary.md           # Market news analysis
├── investment_papers.json    # Research papers found
├── investment_method/
│   ├── investment_idea.md    # Core strategy concept
│   ├── market_anomaly.json   # Identified inefficiency
│   └── trading_strategy.json # Detailed trading rules
├── experiment/
│   ├── backtest.py          # Generated backtest code
│   └── results_summary.json # Performance metrics
├── analysis/
│   ├── performance_analysis.json
│   ├── insights.md
│   └── final_review.md
└── report/
    ├── investment_research_report.md   # Full report
    ├── investment_research_report.html # HTML version
    └── summary_report.md              # Executive summary
```

## ⚙️ Configuration

### LLM Models
- `gpt-4o-mini-2024-07-18`: Fast and cost-effective (default)
- `gpt-4`: Higher quality but slower/expensive

### Customization
Modify research parameters in the pipeline:
- Stock symbols list
- Research focus areas
- Time periods for analysis
- Risk constraints
- Performance targets

## 🔧 Advanced Features

### Custom Subgraph Development
Create new subgraphs by extending `BaseSubgraph`:

```python
from src.airas.core.base import BaseSubgraph
from langgraph.graph import StateGraph

class CustomAnalysisSubgraph(BaseSubgraph):
    def build_graph(self):
        workflow = StateGraph(YourStateClass)
        # Add nodes and edges
        return workflow.compile()
```

### Memory System
AIRAS-Trade maintains context across sessions using the memory system inherited from AIRAS.

## ⚠️ Important Notes

1. **API Costs**: Be mindful of OpenAI API usage, especially with GPT-4
2. **Execution Time**: Full pipeline takes 10-30 minutes depending on complexity
3. **Local Execution**: Backtests run locally, not on GitHub Actions
4. **Risk Disclaimer**: This is for research only, not investment advice

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Run `python fix_langgraph_final.py`
2. **Python Version**: Must use Python 3.10 or 3.11
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **API Key Issues**: Ensure `.env` file has valid keys

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Based on [AIRAS](https://github.com/airas-org/airas) by the AutoRes team
- Uses OpenAI GPT models for AI capabilities
- Market data from Yahoo Finance

## 📞 Support

- Issues: [GitHub Issues](https://github.com/your-org/airas-trade/issues)
- Documentation: This README and code comments

---

**Disclaimer**: AIRAS-Trade is an automated research tool. All investment decisions should be made with proper due diligence and professional advice. Past performance does not guarantee future results.