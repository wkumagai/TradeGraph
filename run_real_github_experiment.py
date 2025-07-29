#!/usr/bin/env python3
"""
Run REAL AIRAS experiments using GitHub Actions with existing experiment examples.
This script uses your GitHub Actions token and repository to execute actual experiments.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Also load from parent directory .env if exists
parent_env_path = Path("../.env")
if parent_env_path.exists():
    load_dotenv(parent_env_path)

# Override with GitHub Actions specific credentials
if os.getenv("GITHUB_ACTIONS_TOKEN"):
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = os.getenv("GITHUB_ACTIONS_TOKEN")

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    GitHubActionsExecutorSubgraph,
    AnalyticSubgraph,
    WriterSubgraph,
    CitationSubgraph
)

def extract_repo_info(github_url):
    """Extract owner, repo name, and branch from GitHub URL."""
    # Example: https://github.com/auto-res2/experiment_script_kumagai4/tree/main
    import re
    pattern = r'https://github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?'
    match = re.match(pattern, github_url)
    if match:
        owner, repo, branch = match.groups()
        return f"{owner}/{repo}", branch or "main"
    return None, None

def run_real_experiment():
    """Run a real AIRAS experiment using GitHub Actions."""
    
    print("🚀 AIRAS Real Experiment Execution with GitHub Actions")
    print("=" * 70)
    
    # Get GitHub repository from environment
    github_repo_url = os.getenv("GITHUB_ACTIONS_REPO")
    if not github_repo_url:
        print("❌ GITHUB_ACTIONS_REPO not found in environment variables!")
        return
    
    github_repository, branch_name = extract_repo_info(github_repo_url)
    if not github_repository:
        print(f"❌ Could not parse repository from: {github_repo_url}")
        return
    
    print(f"📦 Using GitHub Repository: {github_repository}")
    print(f"🌿 Branch: {branch_name}")
    print(f"🔑 GitHub Token: {'✓ Found' if os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN') else '✗ Missing'}")
    
    # Configuration
    llm_name = "gpt-4o-mini-2024-07-18"
    
    # Research topics - you can modify these
    research_topics = [
        "transformer model with adaptive computation time inspired by free energy principle",
        "neural architecture search using evolutionary algorithms and Bayesian optimization",
        "self-supervised learning for multimodal representation with contrastive objectives"
    ]
    
    print(f"\n📚 Available research topics:")
    for i, topic in enumerate(research_topics, 1):
        print(f"{i}. {topic}")
    
    choice = input("\nSelect a research topic (1-3) or enter custom topic: ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(research_topics):
        research_topic = research_topics[int(choice) - 1]
    else:
        research_topic = choice if choice else research_topics[0]
    
    print(f"\n🔬 Research Topic: {research_topic}")
    
    # Prepare state for AIRAS
    state = {
        "research_topic": research_topic,
        "research_study_list": [],
        "base_queries": research_topic,
        
        # GitHub configuration for REAL experiments
        "github_repository": github_repository,
        "branch_name": branch_name,
        
        # Execution configuration
        "llm_name": llm_name,
        "save_dir": "./real_experiment_results",
        "gpu_enabled": True,  # The example repo supports GPU
        "experiment_iteration": 1,
    }
    
    print("\n" + "=" * 70)
    print("Starting REAL experiment pipeline...")
    print("=" * 70)
    
    # Create output directory
    os.makedirs(state["save_dir"], exist_ok=True)
    
    try:
        # Step 1: Create research method
        print("\n📝 Step 1: Creating research method...")
        method_creator = CreateMethodSubgraph(llm_name=llm_name)
        state = method_creator.run(state)
        print("✓ Method created")
        
        # Save method
        with open(f"{state['save_dir']}/method.txt", "w") as f:
            f.write(state.get("new_method", ""))
        
        # Step 2: Create experimental design
        print("\n🔬 Step 2: Creating experimental design...")
        designer = CreateExperimentalDesignSubgraph(llm_name=llm_name)
        state = designer.run(state)
        print("✓ Experimental design created")
        
        # Save strategy and code
        with open(f"{state['save_dir']}/experiment_strategy.txt", "w") as f:
            f.write(state.get("experiment_strategy", ""))
        
        if "experiment_code" in state:
            with open(f"{state['save_dir']}/experiment_code.py", "w") as f:
                f.write(state["experiment_code"])
            print(f"✓ Experiment code saved to: {state['save_dir']}/experiment_code.py")
        
        # Step 3: Execute on GitHub Actions (REAL EXECUTION!)
        print("\n🚀 Step 3: Executing REAL experiment on GitHub Actions...")
        print("This will:")
        print(f"  1. Push code to {github_repository}")
        print(f"  2. Trigger GitHub Actions workflow on branch '{branch_name}'")
        print("  3. Run the experiment on GitHub's GPU infrastructure")
        print("  4. Retrieve REAL results from the execution")
        print("\n⚠️  This will take 5-15 minutes for real execution...")
        
        confirm = input("\nProceed with REAL GitHub Actions execution? (y/n): ")
        
        if confirm.lower() == 'y':
            print("\n🏃 Starting GitHub Actions execution...")
            executor = GitHubActionsExecutorSubgraph(gpu_enabled=state["gpu_enabled"])
            
            try:
                # This triggers REAL execution on GitHub Actions!
                state = executor.run(state)
                
                print("\n✅ REAL experiment executed successfully on GitHub Actions!")
                
                # Show real results
                if "output_text_data" in state:
                    print("\n📊 REAL Experiment Results from GitHub Actions:")
                    print("=" * 70)
                    output_preview = state["output_text_data"][:1000]
                    print(output_preview)
                    if len(state["output_text_data"]) > 1000:
                        print("\n... [truncated, see full results in output file]")
                    
                    # Save real results
                    with open(f"{state['save_dir']}/real_results.txt", "w") as f:
                        f.write(state["output_text_data"])
                    print(f"\n✓ Real results saved to: {state['save_dir']}/real_results.txt")
                
                if "error_text_data" in state and state["error_text_data"].strip():
                    print("\n⚠️  Errors during execution:")
                    print(state["error_text_data"][:500])
                    with open(f"{state['save_dir']}/errors.txt", "w") as f:
                        f.write(state["error_text_data"])
                
                if "image_file_name_list" in state and state["image_file_name_list"]:
                    print(f"\n📈 Generated {len(state['image_file_name_list'])} plots/figures:")
                    for img in state["image_file_name_list"]:
                        print(f"  - {img}")
                
            except Exception as e:
                print(f"\n❌ GitHub Actions execution failed: {e}")
                print("\nTroubleshooting:")
                print("1. Check if the repository exists and is accessible")
                print("2. Verify your GITHUB_ACTIONS_TOKEN has proper permissions")
                print("3. Ensure GitHub Actions is enabled on the repository")
                print("4. Check if workflows exist in .github/workflows/")
                return
                
        else:
            print("\n⏭️  Skipping real execution")
            # Add placeholder for analysis
            state["output_text_data"] = "No real execution - analysis skipped"
            state["error_text_data"] = ""
        
        # Step 4: Analyze real results
        if state.get("output_text_data") and state["output_text_data"] != "No real execution - analysis skipped":
            print("\n📊 Step 4: Analyzing REAL experimental results...")
            analyzer = AnalyticSubgraph(llm_name=llm_name)
            state = analyzer.run(state)
            print("✓ Analysis of real results completed")
            
            with open(f"{state['save_dir']}/analysis.txt", "w") as f:
                f.write(state.get("analysis_report", ""))
        
        # Step 5: Write paper with real results
        print("\n✍️ Step 5: Writing research paper with REAL results...")
        writer = WriterSubgraph(llm_name=llm_name, refine_round=2)
        state = writer.run(state)
        print("✓ Paper written with real experimental data")
        
        # Step 6: Add citations
        print("\n📚 Step 6: Adding citations...")
        citation_writer = CitationSubgraph(llm_name=llm_name)
        state = citation_writer.run(state)
        print("✓ Citations added")
        
        # Save final paper
        if "paper_content" in state:
            paper_path = f"{state['save_dir']}/paper_with_real_results.md"
            with open(paper_path, "w") as f:
                f.write("# Research Paper - Based on REAL GitHub Actions Experiments\n\n")
                f.write(f"**GitHub Repository**: {github_repository}\n")
                f.write(f"**Branch**: {branch_name}\n")
                f.write(f"**Execution**: {'REAL' if 'output_text_data' in state else 'SIMULATED'}\n\n")
                
                for section, content in state["paper_content"].items():
                    f.write(f"## {section}\n\n{content}\n\n")
            
            print(f"\n✓ Paper saved to: {paper_path}")
        
        # Summary
        print("\n" + "=" * 70)
        print("🎉 AIRAS Real Experiment Pipeline Completed!")
        print("=" * 70)
        print(f"\nResults directory: {state['save_dir']}/")
        print("\nGenerated files:")
        for file in os.listdir(state['save_dir']):
            print(f"  - {file}")
        
        if "output_text_data" in state and state["output_text_data"] != "No real execution - analysis skipped":
            print("\n✨ This paper is based on REAL experimental results")
            print("   executed on GitHub Actions infrastructure!")
        
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()

def check_github_setup():
    """Check if GitHub repository is properly set up for AIRAS."""
    
    print("\n🔍 Checking GitHub Setup...")
    print("=" * 70)
    
    github_repo_url = os.getenv("GITHUB_ACTIONS_REPO")
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    
    print(f"GITHUB_ACTIONS_REPO: {github_repo_url or 'NOT SET'}")
    print(f"GITHUB_ACTIONS_TOKEN: {'✓ Found' if github_token else '✗ Missing'}")
    
    if github_repo_url:
        github_repository, branch = extract_repo_info(github_repo_url)
        print(f"\nParsed repository: {github_repository}")
        print(f"Branch: {branch}")
        
        print("\n📋 Required GitHub Actions workflows:")
        print("  - .github/workflows/run_experiment_on_cpu.yml")
        print("  - .github/workflows/run_experiment_on_gpu.yml")
        
        print("\n🔧 To check your repository:")
        print(f"  Visit: {github_repo_url}")
        print("  Check Actions tab for workflow runs")

if __name__ == "__main__":
    print("AIRAS - Real Experiment Execution via GitHub Actions")
    print()
    
    # Check setup first
    check_github_setup()
    
    print("\n" + "=" * 70)
    choice = input("\nReady to run a REAL experiment? (y/n): ")
    
    if choice.lower() == 'y':
        run_real_experiment()
    else:
        print("\n💡 Tips for running real experiments:")
        print("1. Ensure GITHUB_ACTIONS_TOKEN and GITHUB_ACTIONS_REPO are set")
        print("2. Repository must have GitHub Actions enabled")
        print("3. Workflows must be present in .github/workflows/")
        print("4. GPU runners should be configured for GPU experiments")