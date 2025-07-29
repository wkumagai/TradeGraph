#!/usr/bin/env python3
"""
Run AIRAS experiments with the actual GitHub Actions workflow structure.
Fixed version that adapts to the repository's actual workflow.
"""

import os
import sys
import time
import requests
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
parent_env_path = Path("../.env")
if parent_env_path.exists():
    load_dotenv(parent_env_path)

if os.getenv("GITHUB_ACTIONS_TOKEN"):
    os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = os.getenv("GITHUB_ACTIONS_TOKEN")

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    AnalyticSubgraph,
    WriterSubgraph,
    CitationSubgraph
)
from airas.services.api_client.github_client import GithubClient

def trigger_experiment_workflow(github_repository, branch_name, experiment_code):
    """Manually trigger the experiment workflow and retrieve results."""
    
    client = GithubClient()
    github_owner, repository_name = github_repository.split("/", 1)
    
    # First, we need to push the experiment code to the repository
    print("\n📤 Pushing experiment code to repository...")
    
    # Create a new branch for this experiment
    timestamp = int(time.time())
    experiment_branch = f"airas-experiment-{timestamp}"
    
    # Get the default branch SHA
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get reference to main branch
    ref_url = f"https://api.github.com/repos/{github_repository}/git/refs/heads/{branch_name}"
    response = requests.get(ref_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get branch reference: {response.text}")
    
    main_sha = response.json()["object"]["sha"]
    
    # Create new branch
    create_ref_url = f"https://api.github.com/repos/{github_repository}/git/refs"
    ref_data = {
        "ref": f"refs/heads/{experiment_branch}",
        "sha": main_sha
    }
    response = requests.post(create_ref_url, json=ref_data, headers=headers)
    if response.status_code != 201:
        print(f"Warning: Could not create branch: {response.text}")
        experiment_branch = branch_name  # Use existing branch
    else:
        print(f"✓ Created experiment branch: {experiment_branch}")
    
    # Update src/main.py with our experiment code
    file_path = "src/main.py"
    
    # Get current file (if exists) to get SHA
    file_url = f"https://api.github.com/repos/{github_repository}/contents/{file_path}"
    response = requests.get(file_url, headers=headers, params={"ref": experiment_branch})
    
    file_sha = None
    if response.status_code == 200:
        file_sha = response.json()["sha"]
    
    # Prepare the experiment code
    import base64
    encoded_content = base64.b64encode(experiment_code.encode()).decode()
    
    # Create/Update file
    file_data = {
        "message": f"AIRAS experiment code - {timestamp}",
        "content": encoded_content,
        "branch": experiment_branch
    }
    if file_sha:
        file_data["sha"] = file_sha
    
    response = requests.put(file_url, json=file_data, headers=headers)
    if response.status_code not in [200, 201]:
        print(f"Warning: Could not update experiment code: {response.text}")
        # Continue anyway, maybe the workflow will use existing code
    else:
        print(f"✓ Experiment code pushed to {file_path}")
    
    # Trigger the workflow
    print("\n🚀 Triggering GitHub Actions workflow...")
    workflow_dispatch_url = f"https://api.github.com/repos/{github_repository}/actions/workflows/run_experiment.yml/dispatches"
    
    dispatch_data = {
        "ref": experiment_branch
    }
    
    response = requests.post(workflow_dispatch_url, json=dispatch_data, headers=headers)
    if response.status_code != 204:
        print(f"Warning: Workflow dispatch returned: {response.status_code}")
        print(response.text)
    else:
        print("✓ Workflow triggered successfully")
    
    # Wait for workflow to complete
    print("\n⏳ Waiting for workflow to complete...")
    print("This typically takes 5-10 minutes...")
    
    # Poll for workflow completion
    runs_url = f"https://api.github.com/repos/{github_repository}/actions/runs"
    
    start_time = time.time()
    workflow_run_id = None
    
    while True:
        if time.time() - start_time > 900:  # 15 minutes timeout
            print("❌ Timeout waiting for workflow")
            break
        
        response = requests.get(runs_url, headers=headers, params={"branch": experiment_branch, "per_page": 5})
        if response.status_code == 200:
            runs = response.json()["workflow_runs"]
            if runs:
                latest_run = runs[0]
                workflow_run_id = latest_run["id"]
                status = latest_run["status"]
                conclusion = latest_run.get("conclusion")
                
                print(f"\rWorkflow status: {status} | Conclusion: {conclusion or 'pending'}", end="")
                
                if status == "completed":
                    print(f"\n✓ Workflow completed with conclusion: {conclusion}")
                    break
        
        time.sleep(10)
    
    # Download artifacts
    if workflow_run_id:
        print("\n📥 Downloading experiment results...")
        artifacts_url = f"https://api.github.com/repos/{github_repository}/actions/runs/{workflow_run_id}/artifacts"
        
        response = requests.get(artifacts_url, headers=headers)
        if response.status_code == 200:
            artifacts = response.json()["artifacts"]
            
            for artifact in artifacts:
                if artifact["name"] == "experiment-artifacts":
                    # Download artifact
                    download_url = artifact["archive_download_url"]
                    response = requests.get(download_url, headers=headers)
                    
                    if response.status_code == 200:
                        # Save and extract
                        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
                            tmp.write(response.content)
                            tmp_path = tmp.name
                        
                        # Extract
                        import zipfile
                        extract_dir = tempfile.mkdtemp()
                        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_dir)
                        
                        # Read results
                        output_text = ""
                        error_text = ""
                        
                        output_file = Path(extract_dir) / "output.txt"
                        if output_file.exists():
                            output_text = output_file.read_text()
                        
                        error_file = Path(extract_dir) / "error.txt"
                        if error_file.exists():
                            error_text = error_file.read_text()
                        
                        # Clean up
                        os.unlink(tmp_path)
                        shutil.rmtree(extract_dir)
                        
                        print("✓ Results downloaded successfully")
                        return output_text, error_text
    
    return "No results available", "Workflow may have failed"

def run_fixed_experiment():
    """Run AIRAS experiment with fixed GitHub Actions integration."""
    
    print("🚀 AIRAS GitHub Actions Experiment (Fixed Version)")
    print("=" * 70)
    
    github_repository = "auto-res2/experiment_script_kumagai4"
    branch_name = "main"
    
    print(f"📦 Repository: {github_repository}")
    print(f"🌿 Branch: {branch_name}")
    
    # Research topic
    research_topic = "neural ODE-based adaptive transformer with dynamic depth control"
    print(f"\n🔬 Research Topic: {research_topic}")
    
    # Configuration
    llm_name = "gpt-4o-mini-2024-07-18"
    save_dir = f"./github_experiments/{int(time.time())}"
    os.makedirs(save_dir, exist_ok=True)
    
    # Initial state
    state = {
        "research_topic": research_topic,
        "research_study_list": [],
        "base_queries": research_topic,
        "llm_name": llm_name,
        "save_dir": save_dir,
        "github_repository": github_repository,
        "branch_name": branch_name,
    }
    
    try:
        # Step 1: Create method
        print("\n📝 Creating research method...")
        method_creator = CreateMethodSubgraph(llm_name=llm_name)
        state = method_creator.run(state)
        
        with open(f"{save_dir}/method.txt", "w") as f:
            f.write(state.get("new_method", ""))
        
        # Step 2: Create experimental design
        print("\n🔬 Creating experimental design...")
        designer = CreateExperimentalDesignSubgraph(llm_name=llm_name)
        state = designer.run(state)
        
        with open(f"{save_dir}/experiment_strategy.txt", "w") as f:
            f.write(state.get("experiment_strategy", ""))
        
        if "experiment_code" in state:
            with open(f"{save_dir}/experiment_code.py", "w") as f:
                f.write(state["experiment_code"])
            
            # Show code preview
            print("\n📄 Generated code preview:")
            print("-" * 50)
            print(state["experiment_code"][:500])
            print("...")
            print("-" * 50)
        
        # Step 3: Execute on GitHub Actions
        print("\n🚀 Executing on GitHub Actions...")
        
        if "experiment_code" in state:
            output_text, error_text = trigger_experiment_workflow(
                github_repository, 
                branch_name, 
                state["experiment_code"]
            )
            
            # Store results
            state["output_text_data"] = output_text
            state["error_text_data"] = error_text
            
            # Save results
            with open(f"{save_dir}/github_output.txt", "w") as f:
                f.write(output_text)
            
            with open(f"{save_dir}/github_errors.txt", "w") as f:
                f.write(error_text)
            
            print("\n📊 Execution Results:")
            print("=" * 50)
            print(output_text[:1000])
            if len(output_text) > 1000:
                print("... [truncated]")
        
        # Step 4: Analyze results
        print("\n📊 Analyzing results...")
        analyzer = AnalyticSubgraph(llm_name=llm_name)
        state = analyzer.run(state)
        
        with open(f"{save_dir}/analysis.txt", "w") as f:
            f.write(state.get("analysis_report", ""))
        
        # Step 5: Write paper
        print("\n✍️ Writing research paper...")
        writer = WriterSubgraph(llm_name=llm_name, refine_round=1)
        state = writer.run(state)
        
        # Step 6: Add citations
        print("\n📚 Adding citations...")
        citation_writer = CitationSubgraph(llm_name=llm_name)
        state = citation_writer.run(state)
        
        # Save paper
        if "paper_content" in state:
            with open(f"{save_dir}/research_paper.md", "w") as f:
                f.write("# AI Research Paper - GitHub Actions Execution\n\n")
                f.write(f"**Repository**: {github_repository}\n")
                f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for section, content in state["paper_content"].items():
                    f.write(f"## {section}\n\n{content}\n\n")
        
        print("\n" + "=" * 70)
        print("✅ Experiment completed!")
        print(f"Results saved to: {save_dir}/")
        
        # List files
        print("\nGenerated files:")
        for file in os.listdir(save_dir):
            print(f"  - {file}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_fixed_experiment()