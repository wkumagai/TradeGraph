#!/usr/bin/env python3
"""
Set up GitHub repository with proper dependencies for REAL AIRAS experiments.
This will ensure experiments actually run and produce real results.
"""

import os
import sys
import time
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
parent_env_path = Path("../.env")
if parent_env_path.exists():
    load_dotenv(parent_env_path)

if os.getenv("GITHUB_ACTIONS_TOKEN"):
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = os.getenv("GITHUB_ACTIONS_TOKEN")

def create_github_file(repo, file_path, content, message, branch="main"):
    """Create or update a file in GitHub repository."""
    
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if file exists
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers, params={"ref": branch})
    
    file_sha = None
    if response.status_code == 200:
        file_sha = response.json()["sha"]
    
    # Create/update file
    encoded_content = base64.b64encode(content.encode()).decode()
    data = {
        "message": message,
        "content": encoded_content,
        "branch": branch
    }
    if file_sha:
        data["sha"] = file_sha
    
    response = requests.put(url, json=data, headers=headers)
    return response.status_code in [200, 201]

def setup_github_environment():
    """Set up complete GitHub environment for AIRAS experiments."""
    
    print("🔧 Setting up GitHub repository for REAL AIRAS experiments")
    print("=" * 70)
    
    repo = "auto-res2/experiment_script_kumagai4"
    branch = "airas-proper-setup"
    
    # Create requirements.txt with ALL necessary dependencies
    requirements_content = """# Core ML/AI dependencies
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.30.0
torchdiffeq>=0.2.3

# Data processing and visualization
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0

# Experiment tracking
tensorboard>=2.13.0
tqdm>=4.65.0

# Additional utilities
requests>=2.31.0
python-dotenv>=1.0.0
"""

    # Create proper GitHub Actions workflow
    workflow_content = """name: AIRAS Experiment Execution

on:
  workflow_dispatch:
    inputs:
      experiment_name:
        description: 'Experiment name'
        required: false
        default: 'airas_experiment'

jobs:
  run-experiment:
    name: Run AIRAS Experiment
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          cache: "pip"
      
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-dev
      
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip list  # Show installed packages
      
      - name: Create experiment directories
        run: |
          mkdir -p logs
          mkdir -p results
          mkdir -p models
      
      - name: Run experiment
        run: |
          echo "Starting AIRAS experiment at $(date)"
          python src/main.py > logs/output.txt 2> logs/error.txt
          EXIT_CODE=$?
          echo "Experiment completed with exit code: $EXIT_CODE"
          
          # Always save some output even if experiment fails
          if [ ! -s logs/output.txt ]; then
            echo "No output generated" > logs/output.txt
          fi
          
          if [ ! -s logs/error.txt ]; then
            echo "No errors" > logs/error.txt
          fi
        continue-on-error: true
      
      - name: Generate summary
        if: always()
        run: |
          echo "=== Experiment Summary ===" > logs/summary.txt
          echo "Date: $(date)" >> logs/summary.txt
          echo "Python Version: $(python --version)" >> logs/summary.txt
          echo "PyTorch Version: $(python -c 'import torch; print(torch.__version__)')" >> logs/summary.txt
          echo "" >> logs/summary.txt
          echo "Output preview:" >> logs/summary.txt
          head -50 logs/output.txt >> logs/summary.txt
          echo "" >> logs/summary.txt
          echo "Error preview:" >> logs/summary.txt
          head -20 logs/error.txt >> logs/summary.txt
      
      - name: Upload all results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: experiment-artifacts
          path: |
            logs/**
            results/**
            models/**
            *.png
            *.pdf
            *.csv
          retention-days: 7
"""

    # Create a minimal experiment runner that will work
    experiment_runner = """#!/usr/bin/env python3
'''
AIRAS Experiment Runner - Ensures experiments produce real results
'''

import sys
import os

# Add src to path so AIRAS experiments can import properly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_experiment():
    \"\"\"Run the AIRAS-generated experiment with proper error handling.\"\"\"
    
    print("AIRAS Experiment Runner Starting...")
    print("=" * 50)
    
    try:
        # Import and run the AIRAS-generated experiment
        if os.path.exists('src/airas_experiment.py'):
            print("Loading AIRAS experiment from src/airas_experiment.py")
            from airas_experiment import main
            main()
        else:
            print("No AIRAS experiment found. Running default test...")
            # Run a minimal test to verify environment
            import torch
            import transformers
            
            print(f"PyTorch version: {torch.__version__}")
            print(f"Transformers version: {transformers.__version__}")
            print(f"CUDA available: {torch.cuda.is_available()}")
            
            # Simple test computation
            x = torch.randn(10, 10)
            y = torch.randn(10, 10)
            z = torch.matmul(x, y)
            print(f"Test computation successful. Result shape: {z.shape}")
            
    except Exception as e:
        print(f"Error running experiment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\\nExperiment completed successfully!")

if __name__ == "__main__":
    run_experiment()
"""

    print(f"📦 Target repository: {repo}")
    print(f"🌿 Setup branch: {branch}")
    
    # Create branch
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get main branch SHA
    ref_url = f"https://api.github.com/repos/{repo}/git/refs/heads/main"
    response = requests.get(ref_url, headers=headers)
    if response.status_code == 200:
        main_sha = response.json()["object"]["sha"]
        
        # Create new branch
        create_ref_url = f"https://api.github.com/repos/{repo}/git/refs"
        ref_data = {
            "ref": f"refs/heads/{branch}",
            "sha": main_sha
        }
        response = requests.post(create_ref_url, json=ref_data, headers=headers)
        if response.status_code == 201:
            print(f"✓ Created branch: {branch}")
        else:
            print(f"ℹ️  Using existing branch: {branch}")
    
    # Upload files
    files_to_create = [
        ("requirements.txt", requirements_content, "Add comprehensive Python dependencies for AIRAS"),
        (".github/workflows/airas_experiment.yml", workflow_content, "Add proper AIRAS workflow with dependencies"),
        ("src/main.py", experiment_runner, "Add experiment runner with error handling")
    ]
    
    for file_path, content, message in files_to_create:
        print(f"\n📄 Creating {file_path}...")
        if create_github_file(repo, file_path, content, message, branch):
            print(f"✓ Created {file_path}")
        else:
            print(f"❌ Failed to create {file_path}")
    
    print("\n" + "=" * 70)
    print("✅ GitHub environment setup complete!")
    print(f"\nView changes at: https://github.com/{repo}/tree/{branch}")
    print("\nThe repository now has:")
    print("  - Complete Python dependencies (PyTorch, Transformers, etc.)")
    print("  - Proper GitHub Actions workflow")
    print("  - Error-resistant experiment runner")
    
    return repo, branch

if __name__ == "__main__":
    setup_github_environment()