# AIRAS Complete Documentation for Agents

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Core Components](#core-components)
6. [Running Experiments](#running-experiments)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Example Scripts](#example-scripts)
10. [API Reference](#api-reference)

---

## Executive Summary

AIRAS (AI Review Automated System) is an autonomous AI research system that can:
- Generate novel research ideas in AI/ML
- Design and implement experiments
- Execute code on real infrastructure (GitHub Actions)
- Analyze results and write scientific papers
- Produce genuine experimental data, not simulations

**Key Achievement**: AIRAS successfully ran real PyTorch experiments on GPU infrastructure, training a 1.6M parameter transformer model and producing actual convergence data.

---

## System Overview

### Architecture
```
AIRAS Pipeline:
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Method Creation │ --> │ Experiment Design│ --> │ Code Generation │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           |
                                                           v
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ Paper Writing   │ <-- │ Result Analysis  │ <-- │ GitHub Actions  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Key Components
- **CreateMethodSubgraph**: Generates research ideas and methodologies
- **CreateExperimentalDesignSubgraph**: Designs experiments and creates code
- **GitHubActionsExecutorSubgraph**: Executes experiments on real hardware
- **AnalyticSubgraph**: Analyzes experimental results
- **WriterSubgraph**: Writes research papers
- **CitationSubgraph**: Adds academic citations

---

## Installation Guide

### Prerequisites
- Python 3.10 or 3.11 (NOT 3.13+)
- Git
- GitHub account with Actions enabled
- API keys for OpenAI, Anthropic (optional), GitHub

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/airas-org/airas.git
cd airas

# 2. Create virtual environment (MUST use Python 3.11)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install AIRAS
pip install -e .
pip install -e ".[dev]"

# 4. Fix LangGraph compatibility issues
cat > fix_langgraph_final.py << 'EOF'
import os
import re

def fix_imports():
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Fix imports
                content = re.sub(
                    r'from langgraph\.graph\.graph import CompiledGraph',
                    'from typing import Any',
                    content
                )
                content = re.sub(r'-> CompiledGraph:', '-> Any:', content)
                content = re.sub(r': CompiledGraph\b', ': Any', content)
                
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_imports()
EOF

python fix_langgraph_final.py
```

---

## Configuration

### Environment Variables (.env file)
```env
# Required
OPENAI_API_KEY="sk-proj-..."
GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."

# Optional but recommended
ANTHROPIC_API_KEY="sk-ant-..."
DEVIN_API_KEY="apk_user_..."
VERTEX_AI_API_KEY="AIza..."

# For GitHub Actions experiments
GITHUB_ACTIONS_TOKEN="github_pat_..."  # If different from personal token
GITHUB_ACTIONS_REPO="https://github.com/owner/repo"
```

### GitHub Repository Setup

For real experiments, your GitHub repository needs:

1. **Enable GitHub Actions**
   - Go to Settings → Actions → General
   - Enable "Allow all actions"

2. **Create Workflow File** (`.github/workflows/run_experiment.yml`):
```yaml
name: AIRAS Experiment

on:
  workflow_dispatch:

jobs:
  run-experiment:
    runs-on: ubuntu-latest  # or self-hosted for GPU
    timeout-minutes: 30
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: |
          pip install torch torchvision transformers numpy matplotlib
          pip install -r requirements.txt || true
      
      - name: Run experiment
        run: |
          mkdir -p logs results
          python src/main.py > logs/output.txt 2> logs/error.txt || true
        continue-on-error: true
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: experiment-artifacts
          path: |
            logs/**
            results/**
            *.png
            *.pdf
```

3. **Create requirements.txt**:
```txt
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.30.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
scikit-learn>=1.3.0
tqdm>=4.65.0
```

---

## Core Components

### 1. CreateMethodSubgraph
Generates research ideas and methodologies.

```python
from airas.features import CreateMethodSubgraph

method_creator = CreateMethodSubgraph(llm_name="gpt-4o-mini-2024-07-18")
state = method_creator.run({
    "research_topic": "transformer improvements",
    "research_study_list": [],  # Optional: related papers
    "llm_name": "gpt-4o-mini-2024-07-18"
})

# Output: state["new_method"] contains the research methodology
```

### 2. CreateExperimentalDesignSubgraph
Designs experiments and generates implementation code.

```python
from airas.features import CreateExperimentalDesignSubgraph

designer = CreateExperimentalDesignSubgraph(llm_name="gpt-4o-mini-2024-07-18")
state = designer.run(state)  # Uses output from method creator

# Outputs:
# - state["experiment_strategy"]: Experimental design
# - state["experiment_specification"]: Detailed specs
# - state["experiment_code"]: Runnable Python code
```

### 3. GitHubActionsExecutorSubgraph
Executes experiments on real infrastructure.

```python
from airas.features import GitHubActionsExecutorSubgraph

executor = GitHubActionsExecutorSubgraph(gpu_enabled=True)
state["github_repository"] = "owner/repo"
state["branch_name"] = "main"
state["experiment_iteration"] = 1

state = executor.run(state)

# Outputs:
# - state["output_text_data"]: Real experimental results
# - state["error_text_data"]: Any errors during execution
# - state["image_file_name_list"]: Generated plots
```

### 4. AnalyticSubgraph
Analyzes experimental results.

```python
from airas.features import AnalyticSubgraph

analyzer = AnalyticSubgraph(llm_name="gpt-4o-mini-2024-07-18")
state = analyzer.run(state)

# Output: state["analysis_report"] contains analysis
```

### 5. WriterSubgraph
Writes research papers based on results.

```python
from airas.features import WriterSubgraph

# Required fields
state["image_file_name_list"] = []  # Even if no images

writer = WriterSubgraph(llm_name="gpt-4o-mini-2024-07-18", refine_round=2)
state = writer.run(state)

# Output: state["paper_content"] contains paper sections
```

---

## Running Experiments

### Quick Start (Simulated Results)
```python
#!/usr/bin/env python3
"""Quick paper generation without real execution."""

from dotenv import load_dotenv
load_dotenv()

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    WriterSubgraph
)

# Configure
state = {
    "research_topic": "efficient transformers with adaptive computation",
    "research_study_list": [],
    "llm_name": "gpt-4o-mini-2024-07-18",
    "save_dir": "./quick_results"
}

# Generate method
method_creator = CreateMethodSubgraph(llm_name=state["llm_name"])
state = method_creator.run(state)

# Create design
designer = CreateExperimentalDesignSubgraph(llm_name=state["llm_name"])
state = designer.run(state)

# Add dummy results for paper generation
state["output_text_data"] = "Simulated results: Model achieved convergence"
state["analysis_report"] = "The approach shows promise"
state["image_file_name_list"] = []

# Write paper
writer = WriterSubgraph(llm_name=state["llm_name"])
state = writer.run(state)

print("Paper generated (with simulated results)")
```

### Real Experiment Execution
```python
#!/usr/bin/env python3
"""Complete AIRAS pipeline with REAL GitHub Actions execution."""

import os
from dotenv import load_dotenv
load_dotenv()

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    GitHubActionsExecutorSubgraph,
    AnalyticSubgraph,
    WriterSubgraph,
    CitationSubgraph
)

# Configuration
state = {
    "research_topic": "neural ODE-based adaptive transformers",
    "research_study_list": [],
    "llm_name": "gpt-4o-mini-2024-07-18",
    "save_dir": "./real_results",
    
    # GitHub configuration (REQUIRED for real execution)
    "github_repository": "your-org/your-repo",
    "branch_name": "main",
    "gpu_enabled": True,
    "experiment_iteration": 1
}

# Create output directory
os.makedirs(state["save_dir"], exist_ok=True)

print("Step 1: Generating research method...")
method_creator = CreateMethodSubgraph(llm_name=state["llm_name"])
state = method_creator.run(state)

with open(f"{state['save_dir']}/method.txt", "w") as f:
    f.write(state["new_method"])

print("Step 2: Creating experimental design...")
designer = CreateExperimentalDesignSubgraph(llm_name=state["llm_name"])
state = designer.run(state)

with open(f"{state['save_dir']}/experiment_code.py", "w") as f:
    f.write(state["experiment_code"])

print("Step 3: Executing on GitHub Actions (5-15 minutes)...")
executor = GitHubActionsExecutorSubgraph(gpu_enabled=state["gpu_enabled"])
state = executor.run(state)

# Save real results
with open(f"{state['save_dir']}/real_output.txt", "w") as f:
    f.write(state["output_text_data"])

print("Step 4: Analyzing results...")
analyzer = AnalyticSubgraph(llm_name=state["llm_name"])
state = analyzer.run(state)

print("Step 5: Writing paper...")
state["image_file_name_list"] = []  # Required field
writer = WriterSubgraph(llm_name=state["llm_name"])
state = writer.run(state)

print("Step 6: Adding citations...")
citation_writer = CitationSubgraph(llm_name=state["llm_name"])
state = citation_writer.run(state)

# Save paper
if "paper_content" in state:
    with open(f"{state['save_dir']}/paper.md", "w") as f:
        for section, content in state["paper_content"].items():
            f.write(f"## {section}\n\n{content}\n\n")

print(f"\n✅ Complete! Results in: {state['save_dir']}/")
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. LangGraph Import Error
```
ImportError: cannot import name 'CompiledGraph' from 'langgraph.graph.graph'
```
**Solution**: Run the fix script provided in installation.

#### 2. Python Version Error
```
ERROR: Package requires Python >=3.10,<3.13
```
**Solution**: Use Python 3.11 specifically.

#### 3. Missing experiment_specification
```
KeyError: 'experiment_specification'
```
**Solution**: Add to state before WriterSubgraph:
```python
state["experiment_specification"] = "Your experiment details"
```

#### 4. GitHub Actions Not Running
**Check**:
- Repository has Actions enabled
- Workflow file exists in `.github/workflows/`
- GitHub token has workflow permissions
- Branch name is correct

#### 5. No Real Results
**Ensure**:
- Using GitHubActionsExecutorSubgraph
- `github_repository` is set correctly
- Workflow completes successfully
- Dependencies installed in workflow

---

## Best Practices

### 1. **Always Use Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 2. **Save Intermediate Results**
```python
# Save after each step
with open(f"{save_dir}/method.txt", "w") as f:
    f.write(state.get("new_method", ""))
```

### 3. **Handle Errors Gracefully**
```python
try:
    state = executor.run(state)
except Exception as e:
    print(f"Execution failed: {e}")
    # Can still generate paper with partial results
```

### 4. **Monitor GitHub Actions**
```python
print(f"Monitor at: https://github.com/{repo}/actions")
```

### 5. **Use Appropriate LLM**
- `gpt-4o-mini-2024-07-18`: Fast and cost-effective
- `gpt-4`: Better quality but slower/expensive

---

## Example Scripts

### 1. Minimal Setup Checker
```python
#!/usr/bin/env python3
"""Check if AIRAS is properly installed."""

try:
    from airas.features import CreateMethodSubgraph
    print("✅ AIRAS imported successfully")
    
    import torch
    print(f"✅ PyTorch {torch.__version__}")
    
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found")
    else:
        print("❌ OpenAI API key missing")
        
    if os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("✅ GitHub token found")
    else:
        print("❌ GitHub token missing")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

### 2. GitHub Repository Setup
```python
#!/usr/bin/env python3
"""Set up GitHub repository for AIRAS experiments."""

import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def setup_github_repo(repo, branch="main"):
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Requirements.txt content
    requirements = """torch>=2.0.0
transformers>=4.30.0
numpy>=1.24.0
matplotlib>=3.7.0
"""
    
    # Create requirements.txt
    url = f"https://api.github.com/repos/{repo}/contents/requirements.txt"
    data = {
        "message": "Add AIRAS requirements",
        "content": base64.b64encode(requirements.encode()).decode(),
        "branch": branch
    }
    
    response = requests.put(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        print("✅ Created requirements.txt")
    else:
        print(f"❌ Failed: {response.text}")

# Usage
setup_github_repo("owner/repo")
```

### 3. Result Validator
```python
#!/usr/bin/env python3
"""Validate if results are real or simulated."""

def validate_results(output_text):
    """Check if results are from real execution."""
    
    indicators = {
        "real": [
            "PyTorch version:",
            "Device: cuda",
            "Epoch",
            "Loss:",
            "Accuracy:",
            "parameters"
        ],
        "simulated": [
            "92.5%",  # Common dummy value
            "No output generated",
            "Simulated"
        ]
    }
    
    real_count = sum(1 for ind in indicators["real"] if ind in output_text)
    sim_count = sum(1 for ind in indicators["simulated"] if ind in output_text)
    
    if real_count > 3 and sim_count == 0:
        return "REAL"
    elif sim_count > 0:
        return "SIMULATED"
    else:
        return "UNCLEAR"

# Usage
with open("output.txt", "r") as f:
    result_type = validate_results(f.read())
    print(f"Results are: {result_type}")
```

---

## API Reference

### State Dictionary Structure
```python
state = {
    # Required
    "research_topic": str,           # Research topic/question
    "llm_name": str,                 # LLM model to use
    "save_dir": str,                 # Output directory
    
    # Optional
    "research_study_list": list,     # Related papers
    "base_queries": str,             # Search queries
    
    # For GitHub execution
    "github_repository": str,        # "owner/repo"
    "branch_name": str,              # Branch to use
    "gpu_enabled": bool,             # Use GPU runner
    "experiment_iteration": int,     # Experiment number
    
    # Generated (don't set manually)
    "new_method": str,               # From CreateMethodSubgraph
    "experiment_strategy": str,      # From CreateExperimentalDesignSubgraph
    "experiment_specification": str, # From CreateExperimentalDesignSubgraph
    "experiment_code": str,          # From CreateExperimentalDesignSubgraph
    "output_text_data": str,         # From GitHubActionsExecutorSubgraph
    "error_text_data": str,          # From GitHubActionsExecutorSubgraph
    "analysis_report": str,          # From AnalyticSubgraph
    "paper_content": dict,           # From WriterSubgraph
    "image_file_name_list": list,    # Required for WriterSubgraph
}
```

### Subgraph Parameters
```python
# All subgraphs accept
llm_name: str = "gpt-4o-mini-2024-07-18"  # or "gpt-4", "claude-3", etc.

# WriterSubgraph additional params
refine_round: int = 2  # Number of refinement iterations

# GitHubActionsExecutorSubgraph params
gpu_enabled: bool = False  # Whether to use GPU runners
```

---

## Conclusion

AIRAS is a powerful system for automated AI research. With proper setup, it can:
- Generate novel research ideas
- Implement working code
- Run real experiments on GitHub Actions
- Produce genuine scientific results
- Write complete research papers

The key to success is ensuring your GitHub repository is properly configured with dependencies and workflows. Once set up, AIRAS can conduct legitimate AI research autonomously.

For support:
- GitHub Issues: https://github.com/airas-org/airas/issues
- Documentation: https://github.com/airas-org/airas/wiki

Happy researching! 🚀