#!/usr/bin/env python3
"""
Complete AIRAS experiment with GitHub Actions execution.

This script demonstrates how AIRAS actually runs experiments on GitHub Actions,
not just generating placeholder code.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    CreateCodeWithDevinSubgraph,
    GitHubActionsExecutorSubgraph,
    AnalyticSubgraph,
    WriterSubgraph,
    CitationSubgraph
)

def run_complete_airas_experiment():
    """Run a complete AIRAS experiment with real GitHub Actions execution."""
    
    print("🚀 AIRAS Complete Experiment Pipeline")
    print("=" * 70)
    
    # Configuration - YOU NEED TO SET THIS UP
    github_repository = input("Enter your GitHub repository (e.g., username/repo-name): ")
    if not github_repository or github_repository == "username/repo-name":
        print("❌ You must provide a real GitHub repository!")
        print("\nTo use AIRAS with real experiments:")
        print("1. Create a GitHub repository")
        print("2. Add GitHub Actions workflows:")
        print("   - .github/workflows/run_experiment_on_cpu.yml")
        print("   - .github/workflows/run_experiment_on_gpu.yml")
        print("3. Configure secrets in your repository:")
        print("   - Add any API keys needed")
        print("4. Enable GitHub Actions in your repository")
        return
    
    llm_name = "gpt-4o-mini-2024-07-18"
    branch_name = "main"
    
    # Initial state
    state = {
        "research_topic": "transformer model inspired by free energy principle",
        "research_study_list": [],
        "base_queries": "transformer model inspired by free energy principle",
        
        # GitHub configuration for real experiments
        "github_repository": github_repository,
        "branch_name": branch_name,
        
        # LLM and execution configuration
        "llm_name": llm_name,
        "save_dir": "./real_experiment_output",
        "gpu_enabled": False,  # Set to True if your GitHub Actions has GPU runners
        "experiment_iteration": 1,
    }
    
    print(f"Research Topic: {state['research_topic']}")
    print(f"GitHub Repository: {github_repository}")
    print(f"Branch: {branch_name}")
    print("=" * 70)
    
    # Step 1: Create research method
    print("\n📝 Step 1: Creating research method...")
    method_creator = CreateMethodSubgraph(llm_name=llm_name)
    state = method_creator.run(state)
    print("✓ Method created")
    
    # Step 2: Create experimental design
    print("\n🔬 Step 2: Creating experimental design...")
    designer = CreateExperimentalDesignSubgraph(llm_name=llm_name)
    state = designer.run(state)
    print("✓ Experimental design created")
    
    # Step 3: Generate code with Devin (or fallback to standard generation)
    print("\n💻 Step 3: Generating implementation code...")
    try:
        # Try to use Devin if API key is available
        code_creator = CreateCodeWithDevinSubgraph(llm_name=llm_name)
        state = code_creator.run(state)
        print("✓ Code generated with Devin")
    except Exception as e:
        print(f"⚠️  Devin not available ({e}), using standard code generation")
        # Fallback: Use the experiment code from design phase
        if "experiment_code" not in state:
            print("❌ No experiment code generated!")
            return
    
    # Save generated code
    save_dir = state.get('save_dir', './real_experiment_output')
    os.makedirs(save_dir, exist_ok=True)
    
    if "experiment_code" in state:
        code_path = f"{save_dir}/experiment.py"
        with open(code_path, "w") as f:
            f.write(state["experiment_code"])
        print(f"✓ Code saved to: {code_path}")
    
    # Step 4: Execute on GitHub Actions (THIS IS THE REAL EXECUTION)
    print("\n🚀 Step 4: Executing experiment on GitHub Actions...")
    print("This will:")
    print("  1. Push code to your GitHub repository")
    print("  2. Trigger GitHub Actions workflow")
    print("  3. Run the experiment on GitHub's infrastructure")
    print("  4. Retrieve real results")
    
    confirm = input("\nProceed with GitHub Actions execution? (y/n): ")
    if confirm.lower() == 'y':
        executor = GitHubActionsExecutorSubgraph(gpu_enabled=state.get("gpu_enabled", False))
        try:
            state = executor.run(state)
            print("✓ Experiment executed on GitHub Actions!")
            
            # The executor retrieves REAL results from GitHub Actions artifacts
            if "output_text_data" in state:
                print("\n📊 Real Experiment Results:")
                print("-" * 50)
                print(state["output_text_data"][:500] + "..." if len(state["output_text_data"]) > 500 else state["output_text_data"])
                
                # Save real results
                with open(f"{save_dir}/real_results.txt", "w") as f:
                    f.write(state["output_text_data"])
                
            if "error_text_data" in state and state["error_text_data"]:
                print("\n⚠️  Errors during execution:")
                print(state["error_text_data"])
                
        except Exception as e:
            print(f"❌ GitHub Actions execution failed: {e}")
            print("\nMake sure:")
            print("1. Your GitHub repository exists and is accessible")
            print("2. GitHub Actions workflows are properly configured")
            print("3. You have the necessary permissions")
            print("4. Your GITHUB_PERSONAL_ACCESS_TOKEN is valid")
            return
    else:
        print("⏭️  Skipping GitHub Actions execution")
        # Add dummy results for paper generation
        state["output_text_data"] = "Experiment skipped - no real results available"
    
    # Step 5: Analyze results
    print("\n📊 Step 5: Analyzing results...")
    analyzer = AnalyticSubgraph(llm_name=llm_name)
    state = analyzer.run(state)
    print("✓ Analysis completed")
    
    # Step 6: Write paper
    print("\n✍️ Step 6: Writing research paper...")
    writer = WriterSubgraph(llm_name=llm_name, refine_round=2)
    state = writer.run(state)
    print("✓ Paper written")
    
    # Step 7: Add citations
    print("\n📚 Step 7: Adding citations...")
    citation_writer = CitationSubgraph(llm_name=llm_name)
    state = citation_writer.run(state)
    print("✓ Citations added")
    
    # Save all outputs
    print("\n💾 Saving all outputs...")
    
    # Save paper
    if "paper_content" in state:
        with open(f"{save_dir}/paper.md", "w") as f:
            f.write("# Research Paper\n\n")
            for section, content in state["paper_content"].items():
                f.write(f"## {section}\n\n{content}\n\n")
    
    # Save other artifacts
    artifacts = {
        "method.txt": "new_method",
        "experiment_strategy.txt": "experiment_strategy",
        "experiment_code.py": "experiment_code",
        "analysis_report.txt": "analysis_report",
        "real_results.txt": "output_text_data",
        "errors.txt": "error_text_data"
    }
    
    for filename, key in artifacts.items():
        if key in state and state[key]:
            with open(f"{save_dir}/{filename}", "w") as f:
                f.write(str(state[key]))
    
    print("\n" + "=" * 70)
    print("✅ AIRAS experiment pipeline completed!")
    print(f"\nOutputs saved to: {save_dir}")
    print("\nGenerated files:")
    for file in os.listdir(save_dir):
        print(f"  - {file}")
    
    if "output_text_data" in state and state["output_text_data"] != "Experiment skipped - no real results available":
        print("\n🎉 This was a REAL experiment executed on GitHub Actions!")
        print("The results above are from actual code execution, not placeholders.")

def setup_github_actions_workflow():
    """Helper to show how to set up GitHub Actions for AIRAS."""
    
    print("\n📋 GitHub Actions Setup Guide for AIRAS")
    print("=" * 70)
    
    cpu_workflow = """name: Run Experiment on CPU

on:
  workflow_dispatch:
    inputs:
      experiment_iteration:
        description: 'Experiment iteration number'
        required: true
        default: '1'

jobs:
  run-experiment:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install torch torchvision numpy matplotlib scikit-learn
        pip install -r requirements.txt || true
    
    - name: Run experiment
      run: |
        python experiment.py > output.txt 2> error.txt || true
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: experiment-artifacts
        path: |
          output.txt
          error.txt
          *.pdf
          *.png
"""

    gpu_workflow = """name: Run Experiment on GPU

on:
  workflow_dispatch:
    inputs:
      experiment_iteration:
        description: 'Experiment iteration number'
        required: true
        default: '1'

jobs:
  run-experiment:
    runs-on: [self-hosted, gpu]  # Or use cloud GPU runners
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
        pip install -r requirements.txt || true
    
    - name: Run experiment
      run: |
        python experiment.py > output.txt 2> error.txt || true
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: experiment-artifacts
        path: |
          output.txt
          error.txt
          *.pdf
          *.png
"""
    
    print("1. Create these workflow files in your repository:")
    print("\n📄 .github/workflows/run_experiment_on_cpu.yml:")
    print("-" * 50)
    print(cpu_workflow)
    
    print("\n📄 .github/workflows/run_experiment_on_gpu.yml:")
    print("-" * 50)
    print(gpu_workflow)
    
    print("\n2. Configure repository settings:")
    print("   - Enable GitHub Actions in Settings > Actions")
    print("   - Add GITHUB_PERSONAL_ACCESS_TOKEN to repository secrets")
    print("   - Configure GPU runners if using GPU workflows")
    
    print("\n3. The workflow will:")
    print("   - Check out your code")
    print("   - Install dependencies")
    print("   - Run the experiment")
    print("   - Save outputs as artifacts")
    print("   - AIRAS will retrieve these real results")

if __name__ == "__main__":
    print("AIRAS - AI Research Automated System")
    print("This demonstrates REAL experiment execution via GitHub Actions")
    print()
    
    choice = input("1. Run complete experiment\n2. Show GitHub Actions setup guide\nChoice (1/2): ")
    
    if choice == "2":
        setup_github_actions_workflow()
    else:
        run_complete_airas_experiment()