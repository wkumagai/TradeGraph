# TradeGraph GitHub Repository Structure

## Current Repository Contents

The TradeGraph repository (https://github.com/wkumagai/TradeGraph) now contains:

### 📁 Root Directory
```
TradeGraph/
├── README.md                    # Main project overview with quick start
├── requirements.txt             # Python dependencies
├── PROJECT_README.md           # Detailed project documentation
├── .gitignore                  # Git configuration
├── update_imports.py           # Migration script (airas → tradegraph)
└── test_pipeline_simple.py     # Simple test without heavy dependencies
```

### 📁 Source Code (`src/tradegraph/`)
```
src/tradegraph/
├── __init__.py
├── core/                       # Base classes and utilities
├── features/                   # All subgraph implementations
│   ├── stock_research/         # Main pipeline subgraphs
│   ├── analysis/              # Analysis tools
│   ├── create/                # Creation tools
│   ├── execution/             # Execution tools
│   ├── github/                # GitHub integration
│   ├── publication/           # Publishing tools
│   ├── retrieve/              # Data retrieval
│   ├── review/                # Review tools
│   └── write/                 # Writing tools
├── services/                   # API clients
│   └── api_client/
│       ├── alpha_vantage_api.py
│       └── arxiv_api.py
└── types/                      # Type definitions
```

### 📁 Subgraph Organization (`subgraphs/`)
```
subgraphs/
├── README.md                   # Subgraph overview
├── ARCHITECTURE.md            # Technical architecture
├── NAVIGATION.md              # Navigation guide
├── examples/
│   └── run_complete_pipeline.py
│
├── 01_stock_news/             # Market news retrieval
│   ├── README.md              # Component documentation
│   ├── src/                   # Source code
│   ├── tests/                 # Unit tests
│   ├── examples/              # Usage examples
│   └── docs/                  # Additional docs
│
├── 02_investment_papers/      # ArXiv paper search
├── 03_create_investment_method/   # AI strategy generation
├── 04_experiment_planning/    # Backtest design
├── 05_local_execution/        # Code generation
├── 06_results_analysis/       # Performance analysis
└── 07_report_writer/          # Report generation
    └── (same structure as 01)
```

### 📁 Documentation Files
- **Main Documentation**:
  - `README.md` - Quick start and overview
  - `PROJECT_README.md` - Detailed project info
  - `REAL_DATA_VERIFICATION_REPORT.md` - Data source verification

- **Subgraph Documentation**:
  - `subgraphs/README.md` - Pipeline overview
  - `subgraphs/ARCHITECTURE.md` - System design
  - `subgraphs/NAVIGATION.md` - Usage guide
  - Each subgraph has its own README

- **Historical Documentation**:
  - `AIRAS_*.md` files - Original project docs
  - `README_AIRAS_TRADE.md` - Legacy documentation

### 📁 Example Scripts
- **Pipeline Runners**:
  - `run_pipeline_*.py` - Various pipeline configurations
  - `run_real_*.py` - Real data experiments
  - `run_research*.py` - Research pipelines

- **Examples**:
  - `example_*.py` - Usage examples
  - `test_*.py` - Test scripts

- **Utilities**:
  - `generate_paper_*.py` - Report generation
  - `setup_*.py` - Setup scripts

## Key Features on GitHub

### ✅ What's Working
1. **Complete source code** for all 7 subgraphs
2. **Organized structure** with clear separation
3. **Comprehensive documentation** at multiple levels
4. **Example scripts** showing usage
5. **Real data integration** (ArXiv, Alpha Vantage, OpenAI)

### ⚠️ Known Issues
1. **Yahoo Finance RSS** returns 404 (needs alternative)
2. **Some scripts** have old import paths (`src.airas`)
3. **Many duplicate** run scripts with similar functionality

### 🎯 How to Use

1. **Clone and Install**:
   ```bash
   git clone https://github.com/wkumagai/TradeGraph.git
   cd TradeGraph
   pip install -r requirements.txt
   ```

2. **Run Examples**:
   ```bash
   # Complete pipeline
   python subgraphs/examples/run_complete_pipeline.py
   
   # Individual subgraphs
   python subgraphs/01_stock_news/examples/run_stock_news.py
   ```

3. **Navigate Documentation**:
   - Start with `README.md`
   - Check `subgraphs/NAVIGATION.md` for guidance
   - Read individual subgraph READMEs for details

## Summary

The GitHub repository now contains:
- **256 Python files** in organized structure
- **7 main subgraphs** with documentation
- **Multiple examples** and test scripts
- **Clear navigation** and architecture docs
- **Working implementation** with real data sources

The repository is ready for users to clone, understand, and run the TradeGraph pipeline.