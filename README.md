# TradeGraph

TradeGraph is a stock investment research pipeline built with LangGraph that uses real data sources to analyze markets, generate trading strategies, and produce comprehensive investment reports.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/wkumagai/TradeGraph.git
cd TradeGraph

# Install dependencies
pip install -r requirements.txt

# Set up API keys in .env file
OPENAI_API_KEY=your_key_here
ALPHAVANTAGE_API_KEY=your_key_here

# Run the complete pipeline
python subgraphs/examples/run_complete_pipeline.py

# Or run individual subgraphs
python subgraphs/01_stock_news/examples/run_stock_news.py
python subgraphs/02_investment_papers/examples/run_paper_search.py
```

## 📁 Project Structure

```
TradeGraph/
├── src/tradegraph/          # Core implementation
├── subgraphs/              # Modular pipeline components
│   ├── 01_stock_news/      # News retrieval
│   ├── 02_investment_papers/   # Academic paper search
│   ├── 03_create_investment_method/  # Strategy generation
│   ├── 04_experiment_planning/  # Backtest design
│   ├── 05_local_execution/     # Code generation
│   ├── 06_results_analysis/    # Performance analysis
│   ├── 07_report_writer/       # Report generation
│   └── examples/           # Pipeline examples
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔗 Subgraph Documentation

Each subgraph has its own documentation:
- [Stock News](subgraphs/01_stock_news/README.md) - Market news retrieval
- [Investment Papers](subgraphs/02_investment_papers/README.md) - ArXiv paper search
- [Create Method](subgraphs/03_create_investment_method/README.md) - AI strategy generation
- [Experiment Planning](subgraphs/04_experiment_planning/README.md) - Backtest configuration
- [Local Execution](subgraphs/05_local_execution/README.md) - Code generation/execution
- [Results Analysis](subgraphs/06_results_analysis/README.md) - Performance metrics
- [Report Writer](subgraphs/07_report_writer/README.md) - Final report generation

See [Architecture Documentation](subgraphs/ARCHITECTURE.md) for detailed system design.

## Main Pipeline Graph (High-Level)

This graph shows the connections between subgraphs:

```mermaid
graph TD
    %% Styles for subgraphs
    classDef subgraphNode fill:#E3F2FD,stroke:#1565C0,stroke-width:3px,color:#000
    classDef startEnd fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef stateNode fill:#FFD700,stroke:#F57F17,stroke-width:3px,color:#000

    %% Nodes
    START((START)):::startEnd
    State[("Shared State<br/>━━━━━━━━━━<br/>stock_symbols<br/>raw_news<br/>papers<br/>investment_method<br/>results")]:::stateNode
    END((END)):::startEnd
    
    %% Subgraph nodes
    SN[StockNewsSubgraph]:::subgraphNode
    IP[InvestmentPapersSubgraph]:::subgraphNode
    CIM[CreateInvestmentMethodSubgraph]:::subgraphNode
    EP[ExperimentPlanningSubgraph]:::subgraphNode
    LE[LocalExecutionSubgraph]:::subgraphNode
    RA[ResultsAnalysisSubgraph]:::subgraphNode
    RW[ReportWriterSubgraph]:::subgraphNode
    
    %% Main flow
    START --> SN
    START --> IP
    SN --> State
    IP --> State
    State --> CIM
    CIM --> EP
    EP --> LE
    LE --> RA
    RA --> RW
    RW --> END
    
    %% State connections
    CIM -.->|save method| State
    RA -.->|read all data| State
```

## Detailed Subgraph Structures

### 1. StockNewsSubgraph

```mermaid
graph TD
    classDef retrievalNode fill:#81C784,stroke:#388E3C,stroke-width:2px,color:#000
    classDef processNode fill:#AED581,stroke:#689F38,stroke-width:2px,color:#000
    classDef dataSource fill:#E8F5E9,stroke:#4CAF50,stroke-width:1px,color:#1B5E20
    
    subgraph "StockNewsSubgraph"
        START1((ENTRY))
        END1((END))
        
        %% Nodes
        N1[retrieve_stock_news]:::retrievalNode
        N2[filter_relevant_news]:::processNode
        N3[summarize_news]:::processNode
        
        %% Data source
        DS1[Yahoo Finance RSS<br/>❌ 404 Error]:::dataSource
        
        %% Flow
        START1 --> N1
        DS1 -.-> N1
        N1 --> N2
        N2 --> N3
        N3 --> END1
        
        %% Node details
        N1 -.-> |"Fetch RSS feeds<br/>for each symbol"| N1
        N2 -.-> |"Relevance score > 7<br/>Filter by keywords"| N2
        N3 -.-> |"OpenAI API<br/>Generate summary"| N3
    end
```

### 2. InvestmentPapersSubgraph

```mermaid
graph TD
    classDef retrievalNode fill:#81C784,stroke:#388E3C,stroke-width:2px,color:#000
    classDef processNode fill:#AED581,stroke:#689F38,stroke-width:2px,color:#000
    classDef dataSource fill:#E8F5E9,stroke:#4CAF50,stroke-width:1px,color:#1B5E20
    
    subgraph "InvestmentPapersSubgraph"
        START2((ENTRY))
        END2((END))
        
        %% Nodes
        P1[search_papers]:::retrievalNode
        P2[filter_papers]:::processNode
        P3[extract_methods]:::processNode
        
        %% Data source
        DS2[ArXiv API<br/>✅ Working]:::dataSource
        
        %% Flow
        START2 --> P1
        DS2 -.-> P1
        P1 --> P2
        P2 --> P3
        P3 --> END2
        
        %% Node details
        P1 -.-> |"Query: ML trading<br/>portfolio optimization<br/>quant finance"| P1
        P2 -.-> |"Finance keywords<br/>q-fin categories"| P2
        P3 -.-> |"Extract trading<br/>strategies"| P3
    end
```

### 3. CreateInvestmentMethodSubgraph

```mermaid
graph TD
    classDef creationNode fill:#64B5F6,stroke:#1976D2,stroke-width:2px,color:#000
    classDef aiNode fill:#90CAF9,stroke:#1565C0,stroke-width:2px,color:#000
    classDef dataSource fill:#E3F2FD,stroke:#2196F3,stroke-width:1px,color:#0D47A1
    
    subgraph "CreateInvestmentMethodSubgraph"
        START3((ENTRY))
        END3((END))
        
        %% Nodes
        C1[analyze_context]:::creationNode
        C2[generate_strategy]:::aiNode
        C3[validate_method]:::creationNode
        
        %% Data source
        DS3[OpenAI API<br/>✅ GPT-4]:::dataSource
        
        %% Flow
        START3 --> C1
        C1 --> C2
        DS3 -.-> C2
        C2 --> C3
        C3 --> END3
        
        %% Node details
        C1 -.-> |"Analyze news<br/>+ papers"| C1
        C2 -.-> |"Generate trading<br/>strategy"| C2
        C3 -.-> |"Validate<br/>consistency"| C3
    end
```

### 4. ExperimentPlanningSubgraph

```mermaid
graph TD
    classDef planNode fill:#64B5F6,stroke:#1976D2,stroke-width:2px,color:#000
    classDef paramNode fill:#90CAF9,stroke:#1565C0,stroke-width:2px,color:#000
    
    subgraph "ExperimentPlanningSubgraph"
        START4((ENTRY))
        END4((END))
        
        %% Nodes
        E1[plan_experiments]:::planNode
        E2[design_backtest]:::planNode
        E3[set_parameters]:::paramNode
        
        %% Flow
        START4 --> E1
        E1 --> E2
        E2 --> E3
        E3 --> END4
        
        %% Node details
        E1 -.-> |"Define test<br/>scenarios"| E1
        E2 -.-> |"Time periods<br/>Data splits"| E2
        E3 -.-> |"Risk limits<br/>Position sizes"| E3
    end
```

### 5. LocalExecutionSubgraph

```mermaid
graph TD
    classDef execNode fill:#BA68C8,stroke:#7B1FA2,stroke-width:2px,color:#fff
    classDef codeNode fill:#CE93D8,stroke:#8E24AA,stroke-width:2px,color:#000
    
    subgraph "LocalExecutionSubgraph"
        START5((ENTRY))
        END5((END))
        
        %% Nodes
        L1[generate_code]:::codeNode
        L2[prepare_environment]:::execNode
        L3[run_backtest]:::execNode
        
        %% Decision
        D1{Execute?}
        
        %% Flow
        START5 --> L1
        L1 --> L2
        L2 --> D1
        D1 -->|Yes| L3
        D1 -->|No| END5
        L3 --> END5
        
        %% Node details
        L1 -.-> |"Generate Python<br/>backtest code"| L1
        L2 -.-> |"Setup dependencies<br/>Create venv"| L2
        L3 -.-> |"Execute backtest<br/>or skip"| L3
    end
```

### 6. ResultsAnalysisSubgraph

```mermaid
graph TD
    classDef analysisNode fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000
    classDef metricsNode fill:#FFCC80,stroke:#FF6F00,stroke-width:2px,color:#000
    
    subgraph "ResultsAnalysisSubgraph"
        START6((ENTRY))
        END6((END))
        
        %% Nodes
        R1[analyze_performance]:::analysisNode
        R2[calculate_metrics]:::metricsNode
        R3[identify_patterns]:::analysisNode
        
        %% Flow
        START6 --> R1
        R1 --> R2
        R2 --> R3
        R3 --> END6
        
        %% Node details
        R1 -.-> |"Performance<br/>analysis"| R1
        R2 -.-> |"Sharpe ratio<br/>Max drawdown<br/>Returns"| R2
        R3 -.-> |"Pattern<br/>recognition"| R3
    end
```

### 7. ReportWriterSubgraph

```mermaid
graph TD
    classDef reportNode fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    classDef outputNode fill:#FF8A80,stroke:#D32F2F,stroke-width:2px,color:#000
    
    subgraph "ReportWriterSubgraph"
        START7((ENTRY))
        END7((END))
        
        %% Nodes
        W1[compile_results]:::reportNode
        W2[generate_insights]:::reportNode
        W3[create_report]:::outputNode
        
        %% Data source
        DS4[OpenAI API<br/>✅ Analysis]:::dataSource
        
        %% Flow
        START7 --> W1
        W1 --> W2
        DS4 -.-> W2
        W2 --> W3
        W3 --> END7
        
        %% Node details
        W1 -.-> |"Gather all<br/>results"| W1
        W2 -.-> |"AI insights<br/>generation"| W2
        W3 -.-> |"Final report<br/>PDF/HTML"| W3
    end
```

## Data Flow Summary

```mermaid
graph LR
    subgraph "External Data Sources"
        E1[Alpha Vantage API<br/>✅ Stock Prices]
        E2[ArXiv API<br/>✅ Papers]
        E3[Yahoo RSS<br/>❌ News]
        E4[OpenAI API<br/>✅ AI]
    end
    
    subgraph "Pipeline Processing"
        P1[Data Retrieval]
        P2[Strategy Creation]
        P3[Execution]
        P4[Analysis & Report]
    end
    
    E1 --> P1
    E2 --> P1
    E3 -.-> P1
    E4 --> P2
    E4 --> P4
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
```

## Pipeline Status

| Subgraph | Status | Data Source | Output |
|----------|---------|------------|---------|
| StockNewsSubgraph | ⚠️ Needs Fix | Yahoo RSS (404) | News summaries |
| InvestmentPapersSubgraph | ✅ Working | ArXiv API | 6+ papers |
| CreateInvestmentMethodSubgraph | ✅ Working | OpenAI API | Trading strategy |
| ExperimentPlanningSubgraph | ✅ Working | Internal logic | Backtest plan |
| LocalExecutionSubgraph | ✅ Working | Python generation | Executable code |
| ResultsAnalysisSubgraph | ✅ Working | Metrics calculation | Performance stats |
| ReportWriterSubgraph | ✅ Working | OpenAI API | Final report |

## Key Features

- **Hierarchical Structure**: Main graph shows subgraph connections, detailed views show internal nodes
- **Real Data Sources**: All external data is real (no mocks)
- **LangGraph Architecture**: State-based workflow with shared memory
- **Error Resilience**: Pipeline continues despite individual failures
- **Transparent Processing**: Each step clearly shows its data source and processing

---

*This visualization represents the complete hierarchical structure of AIRAS-Trade, from high-level subgraph connections down to individual processing nodes.*
