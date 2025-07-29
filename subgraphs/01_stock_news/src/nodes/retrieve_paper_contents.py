"""Node for retrieving full paper contents."""

import os
import json
from typing import Dict, Any, List
from .....services.api_client.arxiv_client import ArxivClient
from openai import OpenAI


def retrieve_paper_contents_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve full contents of selected investment papers.
    
    This node downloads and extracts content from the most relevant papers.
    """
    paper_titles = state.get("paper_titles", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    if not paper_titles:
        state["paper_contents"] = []
        return state
    
    # Select top papers to retrieve full content
    papers_to_retrieve = paper_titles[:10]  # Limit to top 10
    
    paper_contents = []
    client = OpenAI()
    
    for paper in papers_to_retrieve:
        content_dict = {
            "title": paper.get("title", ""),
            "authors": paper.get("authors", []),
            "published": paper.get("published", ""),
            "source": paper.get("source", ""),
            "abstract": paper.get("abstract", ""),
            "url": paper.get("url", ""),
            "pdf_url": paper.get("pdf_url", "")
        }
        
        # For ArXiv papers, we already have the abstract
        if paper.get("source") == "arxiv" and paper.get("abstract"):
            # Use LLM to analyze the abstract and extract key information
            abstract = paper.get("abstract", "")
            
            prompt = f"""Analyze this investment research paper abstract and extract key information:

Title: {paper.get('title', '')}
Abstract: {abstract}

Extract:
1. Main research question
2. Methodology used
3. Key findings
4. Investment strategy proposed (if any)
5. Performance metrics reported
6. Practical applications
7. Limitations mentioned
8. Data sources and time period

Format as structured JSON."""

            try:
                response = client.chat.completions.create(
                    model=llm_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                analysis = response.choices[0].message.content
                
                # Extract JSON from response
                if "```json" in analysis:
                    analysis = analysis.split("```json")[1].split("```")[0].strip()
                elif "```" in analysis:
                    analysis = analysis.split("```")[1].split("```")[0].strip()
                
                try:
                    content_dict["analysis"] = json.loads(analysis)
                except:
                    content_dict["analysis"] = {"raw": analysis}
            except Exception as e:
                print(f"Error analyzing paper: {e}")
                content_dict["analysis"] = {"error": str(e)}
        
        else:
            # For non-ArXiv papers, generate synthetic analysis based on available info
            prompt = f"""Based on this investment research paper information, provide a detailed analysis:

Title: {paper.get('title', '')}
Authors: {', '.join(paper.get('authors', []))}
Key Findings: {paper.get('key_findings', '')}
Methodology: {paper.get('methodology', '')}

Provide:
1. Likely research objectives
2. Expected methodology details
3. Potential findings and insights
4. Practical trading applications
5. Risk considerations
6. Implementation challenges

Format as structured analysis."""

            try:
                response = client.chat.completions.create(
                    model=llm_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                
                synthetic_analysis = response.choices[0].message.content
                content_dict["analysis"] = {"synthetic": True, "content": synthetic_analysis}
            except Exception as e:
                content_dict["analysis"] = {"error": str(e)}
        
        paper_contents.append(content_dict)
    
    # Update state
    state["paper_contents"] = paper_contents
    
    # Save paper contents
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "paper_contents.json"), "w") as f:
        json.dump(paper_contents, f, indent=2)
    
    print(f"Retrieved content for {len(paper_contents)} papers")
    
    return state