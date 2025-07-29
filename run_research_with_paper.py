#!/usr/bin/env python3
"""Run AIRAS research pipeline with paper generation."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from airas.features import (
    CreateMethodSubgraph,
    CreateExperimentalDesignSubgraph,
    WriterSubgraph,
    CitationSubgraph,
    AnalyticSubgraph,
    LatexSubgraph,
    HtmlSubgraph
)

def run_research_with_paper():
    """Run complete research pipeline including paper generation."""
    
    # Configuration
    llm_name = "gpt-4o-mini-2024-07-18"
    
    # Initial state
    state = {
        # Research topic
        "research_topic": "transformer model inspired by free energy principle",
        "research_study_list": [],  # Would normally contain related papers
        "base_queries": "transformer model inspired by free energy principle",
        
        # Configuration
        "llm_name": llm_name,
        "save_dir": "./research_output_with_paper",
        "gpu_enabled": True,
        "experiment_iteration": 1,
        
        # GitHub configuration (for LaTeX/HTML publishing)
        "github_owner": "your-username",
        "repository_name": "airas-papers",
        "branch_name": "main"
    }
    
    print("🚀 Starting AIRAS Research Pipeline with Paper Generation")
    print("=" * 70)
    print(f"Research Topic: {state['research_topic']}")
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
    
    # Step 3: Simulate some results for the paper
    # In real scenario, this would come from actual experiments
    state["output_text_data"] = """
    Experiment Results:
    - Cross-modal Transformer with FEP achieved 92.5% accuracy on multimodal tasks
    - Baseline Transformer achieved 85.3% accuracy
    - FEP module reduced uncertainty by 35% compared to baseline
    - Model showed superior adaptation to out-of-distribution samples
    """
    state["image_file_name_list"] = []  # Would contain result plots
    
    # Step 4: Analyze results
    print("\n📊 Step 4: Analyzing results...")
    analyzer = AnalyticSubgraph(llm_name=llm_name)
    state = analyzer.run(state)
    print("✓ Analysis completed")
    
    # Step 5: Write the paper
    print("\n✍️ Step 5: Writing research paper...")
    writer = WriterSubgraph(llm_name=llm_name, refine_round=2)
    state = writer.run(state)
    print("✓ Paper written")
    
    # Step 6: Add citations
    print("\n📚 Step 6: Adding citations...")
    citation_writer = CitationSubgraph(llm_name=llm_name)
    state = citation_writer.run(state)
    print("✓ Citations added")
    
    # Save outputs
    save_dir = state.get('save_dir', './research_output_with_paper')
    os.makedirs(save_dir, exist_ok=True)
    
    # Save method
    if "new_method" in state:
        with open(f"{save_dir}/method.txt", "w") as f:
            f.write(state["new_method"])
    
    # Save experimental design
    if "experiment_strategy" in state:
        with open(f"{save_dir}/experiment_strategy.txt", "w") as f:
            f.write(state["experiment_strategy"])
    
    # Save experiment code
    if "experiment_code" in state:
        with open(f"{save_dir}/experiment_code.py", "w") as f:
            f.write(state["experiment_code"])
    
    # Save analysis
    if "analysis_report" in state:
        with open(f"{save_dir}/analysis_report.txt", "w") as f:
            f.write(state["analysis_report"])
    
    # Save paper
    if "paper_content" in state:
        # Save as text sections
        with open(f"{save_dir}/paper.txt", "w") as f:
            paper = state["paper_content"]
            f.write("RESEARCH PAPER\n")
            f.write("=" * 70 + "\n\n")
            for section, content in paper.items():
                f.write(f"\n{section}\n")
                f.write("-" * len(section) + "\n")
                f.write(content + "\n")
        
        # Save individual sections
        paper_sections_dir = f"{save_dir}/paper_sections"
        os.makedirs(paper_sections_dir, exist_ok=True)
        for section, content in paper.items():
            safe_filename = section.replace(" ", "_").replace("/", "_")
            with open(f"{paper_sections_dir}/{safe_filename}.txt", "w") as f:
                f.write(content)
    
    # Save references
    if "references" in state:
        with open(f"{save_dir}/references.txt", "w") as f:
            f.write("\n".join(state["references"]))
    
    print("\n" + "=" * 70)
    print("✅ Research pipeline with paper generation completed!")
    print(f"Results saved to: {save_dir}")
    print("\nGenerated files:")
    print(f"  - Method: {save_dir}/method.txt")
    print(f"  - Strategy: {save_dir}/experiment_strategy.txt")
    print(f"  - Code: {save_dir}/experiment_code.py")
    print(f"  - Analysis: {save_dir}/analysis_report.txt")
    print(f"  - Paper: {save_dir}/paper.txt")
    print(f"  - Paper sections: {save_dir}/paper_sections/")
    print(f"  - References: {save_dir}/references.txt")
    
    # Optional: Generate LaTeX version
    if input("\nGenerate LaTeX version? (y/n): ").lower() == 'y':
        print("\n📄 Generating LaTeX paper...")
        latex_generator = LatexSubgraph()
        state = latex_generator.run(state)
        print("✓ LaTeX paper generated")
    
    # Optional: Generate HTML version
    if input("\nGenerate HTML version? (y/n): ").lower() == 'y':
        print("\n🌐 Generating HTML paper...")
        html_generator = HtmlSubgraph()
        state = html_generator.run(state)
        print("✓ HTML paper generated")
    
    return state

if __name__ == "__main__":
    final_state = run_research_with_paper()
    
    print("\n📊 Summary:")
    print(f"- Research topic: {final_state.get('research_topic', 'N/A')}")
    print(f"- Paper sections: {list(final_state.get('paper_content', {}).keys())}")
    print(f"- References: {len(final_state.get('references', []))}")