# TradeGraph Navigation Guide

This guide helps you navigate the TradeGraph project structure and understand how to use each component.

## 🗺️ Quick Navigation

### For Users

1. **Want to run the complete pipeline?**
   ```bash
   python subgraphs/examples/run_complete_pipeline.py
   ```

2. **Want to test individual components?**
   - Stock News: `python subgraphs/01_stock_news/examples/run_stock_news.py`
   - Paper Search: `python subgraphs/02_investment_papers/examples/run_paper_search.py`

3. **Want to understand the architecture?**
   - Start with [ARCHITECTURE.md](ARCHITECTURE.md)
   - Then read individual subgraph READMEs

### For Developers

1. **Adding a new subgraph?**
   - Create directory: `subgraphs/XX_your_feature/`
   - Follow structure in existing subgraphs
   - Update pipeline in `examples/run_complete_pipeline.py`

2. **Modifying existing subgraph?**
   - Go to `subgraphs/XX_name/src/`
   - Run tests: `pytest subgraphs/XX_name/tests/`
   - Update examples if needed

3. **Core implementation?**
   - Main code: `src/tradegraph/`
   - Subgraph base: `src/tradegraph/core/base.py`

## 📊 Pipeline Flow

```
1. Data Retrieval (Parallel)
   ├── 01_stock_news → Get market news
   └── 02_investment_papers → Get research papers

2. Strategy Creation
   ├── 03_create_investment_method → Generate AI strategy
   └── 04_experiment_planning → Design backtest

3. Execution
   └── 05_local_execution → Generate/run code

4. Analysis & Reporting
   ├── 06_results_analysis → Analyze performance
   └── 07_report_writer → Create final report
```

## 🔧 Configuration

### Required API Keys
- `OPENAI_API_KEY` - For AI analysis (GPT-4)
- `ALPHAVANTAGE_API_KEY` - For stock data

### Optional Configuration
- Edit subgraph parameters in individual example files
- Modify pipeline flow in `run_complete_pipeline.py`

## 📚 Documentation Hierarchy

```
README.md                    # Project overview
├── subgraphs/README.md     # Subgraph system overview
├── subgraphs/ARCHITECTURE.md   # Technical architecture
├── subgraphs/NAVIGATION.md    # This file
└── subgraphs/XX_*/README.md   # Individual subgraph docs
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Subgraph Tests
```bash
pytest subgraphs/01_stock_news/tests/
```

### Run Integration Test
```bash
python test_pipeline_simple.py
```

## 🚀 Common Tasks

### Generate a Trading Strategy
```python
from src.tradegraph.features.stock_research import (
    InvestmentPapersSubgraph,
    CreateInvestmentMethodSubgraph
)

# Get papers
papers = InvestmentPapersSubgraph().run({"papers": []})

# Generate strategy
strategy = CreateInvestmentMethodSubgraph().run({
    "papers": papers["papers"],
    "stock_symbols": ["AAPL", "GOOGL"]
})
```

### Analyze Stock News
```python
from src.tradegraph.features.stock_research import StockNewsSubgraph

news = StockNewsSubgraph().run({
    "stock_symbols": ["AAPL"],
    "raw_news": [],
    "filtered_news": [],
    "news_summary": ""
})
```

## 📈 Output Examples

### Pipeline Output Structure
```
pipeline_output_YYYYMMDD_HHMMSS/
├── state.json          # Complete pipeline state
├── report.md          # Final investment report
└── backtest_code.py   # Generated trading code
```

### Individual Subgraph Outputs
- Stock News: `news_results_*.json`
- Papers: `papers_results_*.json`
- Full Pipeline: `pipeline_output_*/`

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'tradegraph'"**
   - Run from project root directory
   - Or add to PYTHONPATH: `export PYTHONPATH=$PYTHONPATH:$(pwd)`

2. **API Key Errors**
   - Create `.env` file with your keys
   - Or export: `export OPENAI_API_KEY=your_key`

3. **Yahoo News 404 Error**
   - Known issue - Yahoo RSS returns 404
   - Pipeline continues with other data sources

## 🤝 Contributing

1. Pick a subgraph to improve
2. Read its README and understand the flow
3. Make changes in `subgraphs/XX_name/src/`
4. Add tests in `subgraphs/XX_name/tests/`
5. Update examples and documentation
6. Submit PR with clear description