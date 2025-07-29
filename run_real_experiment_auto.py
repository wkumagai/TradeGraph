#!/usr/bin/env python3
"""
Automatically run REAL AIRAS experiments using GitHub Actions.
This runs without user interaction using your configured GitHub repository.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
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
    import re
    pattern = r'https://github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?'
    match = re.match(pattern, github_url)
    if match:
        owner, repo, branch = match.groups()
        return f"{owner}/{repo}", branch or "main"
    return None, None

def run_automatic_experiment():
    """Run AIRAS experiment automatically without user interaction."""
    
    print("🚀 AIRAS Automated Real Experiment Execution")
    print("=" * 70)
    
    # Get GitHub repository configuration
    github_repo_url = os.getenv("GITHUB_ACTIONS_REPO")
    github_repository, branch_name = extract_repo_info(github_repo_url)
    
    print(f"📦 Repository: {github_repository}")
    print(f"🌿 Branch: {branch_name}")
    print(f"🔑 GitHub Token: {'✓ Found' if os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN') else '✗ Missing'}")
    
    # Use a specific research topic
    research_topic = "transformer model with adaptive computation time using neural ODE dynamics"
    
    print(f"\n🔬 Research Topic: {research_topic}")
    
    # Configuration
    llm_name = "gpt-4o-mini-2024-07-18"
    save_dir = f"./real_experiments/{int(time.time())}"
    
    # Initial state for AIRAS
    state = {
        "research_topic": research_topic,
        "research_study_list": [],
        "base_queries": research_topic,
        
        # GitHub configuration for REAL experiments
        "github_repository": github_repository,
        "branch_name": branch_name,
        
        # Execution configuration
        "llm_name": llm_name,
        "save_dir": save_dir,
        "gpu_enabled": False,  # Use CPU workflow (change to True for GPU)
        "experiment_iteration": 1,
    }
    
    print(f"\n💾 Results will be saved to: {save_dir}")
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        # Step 1: Create research method
        print("\n📝 Step 1: Creating research method...")
        method_creator = CreateMethodSubgraph(llm_name=llm_name)
        state = method_creator.run(state)
        print("✓ Method created successfully")
        
        # Save method
        with open(f"{save_dir}/method.txt", "w") as f:
            f.write(state.get("new_method", ""))
        
        # Step 2: Create experimental design and code
        print("\n🔬 Step 2: Creating experimental design...")
        designer = CreateExperimentalDesignSubgraph(llm_name=llm_name)
        state = designer.run(state)
        print("✓ Experimental design created")
        
        # Save experimental artifacts
        with open(f"{save_dir}/experiment_strategy.txt", "w") as f:
            f.write(state.get("experiment_strategy", ""))
        
        if "experiment_code" in state:
            with open(f"{save_dir}/experiment_code.py", "w") as f:
                f.write(state["experiment_code"])
            print(f"✓ Experiment code generated: {save_dir}/experiment_code.py")
        
        # Show a preview of the generated code
        if "experiment_code" in state:
            print("\n📄 Generated experiment code preview:")
            print("-" * 50)
            code_lines = state["experiment_code"].split('\n')[:20]
            for line in code_lines:
                print(line)
            print("... [truncated]")
            print("-" * 50)
        
        # Step 3: Execute on GitHub Actions (REAL EXECUTION!)
        print("\n🚀 Step 3: Executing REAL experiment on GitHub Actions...")
        print(f"⏳ This will take approximately 5-15 minutes...")
        print(f"📍 Monitor progress at: https://github.com/{github_repository}/actions")
        
        start_time = time.time()
        executor = GitHubActionsExecutorSubgraph(gpu_enabled=state["gpu_enabled"])
        
        print("\n🏃 Triggering GitHub Actions workflow...")
        state = executor.run(state)
        
        execution_time = time.time() - start_time
        print(f"\n✅ GitHub Actions execution completed in {execution_time/60:.1f} minutes!")
        
        # Process and display real results
        if "output_text_data" in state:
            print("\n📊 REAL Experiment Results from GitHub Actions:")
            print("=" * 70)
            
            # Show first 1500 characters of results
            output_preview = state["output_text_data"][:1500]
            print(output_preview)
            
            if len(state["output_text_data"]) > 1500:
                print("\n... [See full results in output file]")
            
            # Save complete results
            with open(f"{save_dir}/github_actions_output.txt", "w") as f:
                f.write(state["output_text_data"])
            
            print(f"\n✓ Full results saved to: {save_dir}/github_actions_output.txt")
        
        # Check for errors
        if "error_text_data" in state and state["error_text_data"].strip():
            print("\n⚠️  Execution errors/warnings:")
            error_preview = state["error_text_data"][:500]
            print(error_preview)
            
            with open(f"{save_dir}/execution_errors.txt", "w") as f:
                f.write(state["error_text_data"])
        
        # Check for generated figures
        if "image_file_name_list" in state and state["image_file_name_list"]:
            print(f"\n📈 Generated {len(state['image_file_name_list'])} visualizations:")
            for img in state["image_file_name_list"]:
                print(f"  - {img}")
        
        # Step 4: Analyze real results
        print("\n📊 Step 4: Analyzing REAL experimental results...")
        analyzer = AnalyticSubgraph(llm_name=llm_name)
        state = analyzer.run(state)
        print("✓ Analysis completed")
        
        with open(f"{save_dir}/analysis_report.txt", "w") as f:
            f.write(state.get("analysis_report", ""))
        
        # Step 5: Generate research paper with real results
        print("\n✍️ Step 5: Writing research paper based on REAL results...")
        writer = WriterSubgraph(llm_name=llm_name, refine_round=2)
        state = writer.run(state)
        print("✓ Paper written")
        
        # Step 6: Add citations
        print("\n📚 Step 6: Adding citations...")
        citation_writer = CitationSubgraph(llm_name=llm_name)
        state = citation_writer.run(state)
        print("✓ Citations added")
        
        # Save the final paper
        if "paper_content" in state:
            paper_path = f"{save_dir}/research_paper.md"
            with open(paper_path, "w") as f:
                f.write("# AI Research Paper - Based on REAL GitHub Actions Experiments\n\n")
                f.write("---\n\n")
                f.write(f"**Repository**: [{github_repository}](https://github.com/{github_repository})\n")
                f.write(f"**Branch**: {branch_name}\n")
                f.write(f"**Execution Time**: {execution_time/60:.1f} minutes\n")
                f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                for section, content in state["paper_content"].items():
                    f.write(f"## {section}\n\n")
                    f.write(content)
                    f.write("\n\n")
            
            print(f"\n✓ Research paper saved to: {paper_path}")
        
        # Final summary
        print("\n" + "=" * 70)
        print("🎉 AIRAS Real Experiment Pipeline Completed Successfully!")
        print("=" * 70)
        
        print(f"\n📂 All results saved in: {save_dir}/")
        print("\n📄 Generated files:")
        for file in sorted(os.listdir(save_dir)):
            file_size = os.path.getsize(f"{save_dir}/{file}")
            print(f"  - {file:<30} ({file_size:,} bytes)")
        
        print("\n✨ Key Achievement:")
        print("This research paper is based on REAL experimental results")
        print("executed on GitHub Actions infrastructure, not simulated data!")
        
        return state
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("AIRAS - Automated Real Experiment Execution")
    print("This will run a complete experiment on GitHub Actions\n")
    
    # Check prerequisites
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("❌ Error: GITHUB_PERSONAL_ACCESS_TOKEN not found!")
        print("Please set your GitHub token in the environment variables.")
        sys.exit(1)
    
    if not os.getenv("GITHUB_ACTIONS_REPO"):
        print("❌ Error: GITHUB_ACTIONS_REPO not found!")
        print("Please set your GitHub repository URL in the environment variables.")
        sys.exit(1)
    
    # Run the experiment
    result = run_automatic_experiment()
    
    if result:
        print("\n✅ Experiment completed successfully!")
        print(f"Check the results in: {result['save_dir']}/")
    else:
        print("\n❌ Experiment failed. Please check the error messages above.")