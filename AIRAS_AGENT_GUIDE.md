# AIRAS Setup and Usage Guide for Agents

## 🚀 Quick Summary

AIRAS (AI Review Automated System) is a powerful tool that can automatically conduct AI research - from generating ideas to running real experiments on GitHub Actions. Here's what you need to know to use it smoothly.

## 📋 Prerequisites

### 1. **Environment Setup**
```bash
# Clone AIRAS
git clone https://github.com/airas-org/airas.git
cd airas

# Create Python 3.11 virtual environment (IMPORTANT: Not 3.13!)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
pip install -e ".[dev]"
```

### 2. **Required API Keys**
Create `.env` file with:
```env
OPENAI_API_KEY="your-key"
ANTHROPIC_API_KEY="your-key"
DEVIN_API_KEY="your-key"  # Optional but recommended
GITHUB_PERSONAL_ACCESS_TOKEN="your-github-token"
VERTEX_AI_API_KEY="your-key"  # Optional
```

### 3. **GitHub Repository Setup**
For real experiments, you need:
- A GitHub repository with Actions enabled
- Proper workflow files (see setup script below)
- GitHub token with workflow permissions

## 🔧 Key Issues and Solutions

### 1. **LangGraph Import Errors**
AIRAS has outdated imports. Fix with:
```bash
python fix_langgraph_final.py
```

### 2. **Missing Dependencies in Target Repository**
Many GitHub repos lack PyTorch/ML dependencies. Use:
```python
# This script sets up proper dependencies
python setup_github_for_real_experiments.py
```

### 3. **WriterSubgraph Errors**
Add missing fields to state:
```python
state["experiment_specification"] = "Your experiment specs"
state["image_file_name_list"] = []  # Even if empty
```

## 🎯 How to Run Real Experiments

### Option 1: Simple Paper Generation (No Real Execution)
```python
#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

from airas.features import CreateMethodSubgraph, CreateExperimentalDesignSubgraph

# Generate research idea and code
state = {
    "research_topic": "your AI research topic",
    "llm_name": "gpt-4o-mini-2024-07-18",
    "save_dir": "./output"
}

# Generate method and code
method_creator = CreateMethodSubgraph(llm_name=state["llm_name"])
state = method_creator.run(state)

designer = CreateExperimentalDesignSubgraph(llm_name=state["llm_name"])
state = designer.run(state)
```

### Option 2: Real Experiment with GitHub Actions
```python
from airas.features import GitHubActionsExecutorSubgraph

# After generating code, execute it
executor = GitHubActionsExecutorSubgraph(gpu_enabled=True)
state["github_repository"] = "owner/repo"
state["branch_name"] = "main"

# This triggers REAL execution on GitHub!
state = executor.run(state)

# state["output_text_data"] now contains REAL results
```

## 📁 Output Structure

AIRAS generates:
```
./research_output/
├── method.txt              # Research methodology
├── experiment_strategy.txt # Experimental design
├── experiment_code.py      # Generated code
└── paper/
    ├── paper.md           # Full research paper
    └── summary.txt        # Executive summary
```

## ⚠️ Common Pitfalls

1. **Dummy Results**: Without GitHubActionsExecutorSubgraph, results are simulated
2. **Python Version**: Must use Python <3.13 (3.11 recommended)
3. **Missing Dependencies**: Target GitHub repo needs proper requirements.txt
4. **API Limits**: Be mindful of OpenAI API usage

## 🚀 Complete Working Example

```python
#!/usr/bin/env python3
"""Run complete AIRAS experiment with real results."""

import os
from dotenv import load_dotenv
load_dotenv()

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    GitHubActionsExecutorSubgraph,
    AnalyticSubgraph,
    WriterSubgraph
)

# Configuration
state = {
    "research_topic": "adaptive transformer with neural ODEs",
    "research_study_list": [],
    "llm_name": "gpt-4o-mini-2024-07-18",
    "save_dir": "./results",
    "github_repository": "your-org/your-repo",
    "branch_name": "main",
    "gpu_enabled": True,
    "experiment_iteration": 1
}

# 1. Generate research method
method_creator = CreateMethodSubgraph(llm_name=state["llm_name"])
state = method_creator.run(state)

# 2. Create experimental design
designer = CreateExperimentalDesignSubgraph(llm_name=state["llm_name"])
state = designer.run(state)

# 3. Execute on GitHub Actions (REAL RESULTS!)
executor = GitHubActionsExecutorSubgraph(gpu_enabled=True)
state = executor.run(state)  # This runs REAL experiments!

# 4. Analyze real results
analyzer = AnalyticSubgraph(llm_name=state["llm_name"])
state = analyzer.run(state)

# 5. Write paper
state["image_file_name_list"] = []  # Required field
writer = WriterSubgraph(llm_name=state["llm_name"])
state = writer.run(state)

print(f"Results saved to: {state['save_dir']}")
```

## 📊 Real vs Simulated Results

- **Real Results**: Use GitHubActionsExecutorSubgraph - takes 5-15 minutes
- **Simulated Results**: Skip executor - instant but fake data
- **How to Tell**: Real results have actual training logs, loss curves, timestamps

## 🛠️ GitHub Repository Requirements

Your target repository needs:

### 1. Workflow file (`.github/workflows/run_experiment.yml`):
```yaml
name: Run Experiment
on: workflow_dispatch

jobs:
  run-experiment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: |
          pip install torch transformers numpy matplotlib
          
      - name: Run experiment
        run: |
          python src/main.py > logs/output.txt 2> logs/error.txt
          
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: experiment-artifacts
          path: logs/**
```

### 2. Requirements file:
```txt
torch>=2.0.0
transformers>=4.30.0
numpy>=1.24.0
matplotlib>=3.7.0
```

## ✅ Success Indicators

You know AIRAS is working when:
1. GitHub Actions workflow triggers successfully
2. Real training logs appear (losses, accuracies)
3. Execution takes 5-15 minutes (not instant)
4. Results contain timestamps and hardware info
5. Analysis references actual metrics, not placeholders

## 📞 Need Help?

- AIRAS Issues: https://github.com/airas-org/airas/issues
- Common fix: Run `fix_langgraph_final.py` for import errors
- Check Python version: Must be <3.13
- Verify GitHub token has workflow permissions

---

**Remember**: AIRAS can generate ideas and code quickly, but real experiments require proper GitHub setup and take time to execute. The effort is worth it for genuine research results!