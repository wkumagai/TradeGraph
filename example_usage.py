#!/usr/bin/env python3
"""Example usage of AIRAS for automated research."""

from airas.features import (
    PrepareRepositorySubgraph,
    RetrieveCodeSubgraph, 
    CreateExperimentalDesignSubgraph, 
    CreateMethodSubgraph,
    GitHubActionsExecutorSubgraph,
    FixCodeWithDevinSubgraph
)

def simple_research_workflow():
    """Run a simple research workflow using AIRAS."""
    
    # Configuration
    llm_name = "openai:gpt-4o-mini"  # You can also use other models
    save_dir = "./research_output"
    
    print("Starting AIRAS Research Workflow")
    print("=" * 50)
    
    # Initialize state with research topic
    state = {
        "base_queries": "diffusion model optimization",
        "gpu_enabled": True,
        "experiment_iteration": 1,
        "llm_name": llm_name,
        "save_dir": save_dir
    }
    
    # Step 1: Create research method
    print("\n1. Creating research method...")
    method_creator = CreateMethodSubgraph(llm_name=llm_name)
    state = method_creator.run(state)
    if "new_method" in state:
        print(f"✓ Method created: {state['new_method'][:100]}...")
    
    # Step 2: Create experimental design
    print("\n2. Creating experimental design...")
    design_creator = CreateExperimentalDesignSubgraph(llm_name=llm_name)
    state = design_creator.run(state)
    if "experiment_strategy" in state:
        print(f"✓ Design created: {state['experiment_strategy'][:100]}...")
    
    # Step 3: Retrieve relevant code (if needed)
    print("\n3. Retrieving relevant code examples...")
    code_retriever = RetrieveCodeSubgraph(llm_name=llm_name)
    # Note: This would typically need additional state like paper references
    # state = code_retriever.run(state)
    print("✓ Code retrieval configured (skipped in demo)")
    
    print("\n" + "=" * 50)
    print("Research workflow completed!")
    print("\nNext steps:")
    print("- Implement the proposed method")
    print("- Run experiments using GitHubActionsExecutorSubgraph")
    print("- Analyze results and iterate")
    
    return state

def advanced_workflow_with_github():
    """Example of using AIRAS with GitHub integration."""
    
    print("\nAdvanced Workflow with GitHub Integration")
    print("=" * 50)
    
    # Configuration for GitHub
    github_config = {
        "github_owner": "your-github-username",
        "repository_name": "airas-experiments",
        "branch_name": "main",
        "llm_name": "openai:gpt-4o-mini"
    }
    
    # Prepare repository
    print("\n1. Preparing GitHub repository...")
    repo_preparer = PrepareRepositorySubgraph()
    # This would create/prepare your GitHub repository
    # state = repo_preparer.run(github_config)
    print("✓ Repository preparation configured")
    
    # Execute experiments with GitHub Actions
    print("\n2. Setting up GitHub Actions execution...")
    executor = GitHubActionsExecutorSubgraph()
    # This would run experiments using GitHub Actions
    # state = executor.run(state)
    print("✓ GitHub Actions executor configured")
    
    print("\nGitHub integration ready for automated experiments!")

if __name__ == "__main__":
    # Run simple workflow
    simple_research_workflow()
    
    # Show advanced workflow
    advanced_workflow_with_github()
    
    print("\n" + "=" * 50)
    print("AIRAS Demo Complete!")
    print("\nTo run a full research pipeline:")
    print("1. Configure all API keys in .env")
    print("2. Set up GitHub repository access")
    print("3. Customize the workflow for your research needs")
    print("4. Run the complete pipeline with all subgraphs")