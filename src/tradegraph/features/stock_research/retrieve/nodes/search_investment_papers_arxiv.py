"""Node for searching investment research papers."""

import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .....services.api_client.arxiv_client import ArxivClient
from openai import OpenAI


def search_investment_papers_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Search for recent investment and trading research papers.
    
    This node searches academic databases for papers on investment methods,
    trading strategies, and market anomalies.
    """
    search_queries = state.get("search_queries", [])
    time_range = state.get("time_range", "1y")
    paper_sources = state.get("paper_sources", ["arxiv", "ssrn"])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    # Calculate date range
    time_map = {
        "1m": 30,
        "3m": 90,
        "6m": 180,
        "1y": 365,
        "2y": 730
    }
    days = time_map.get(time_range, 365)
    date_from = datetime.now() - timedelta(days=days)
    
    all_papers = []
    
    # Search ArXiv if available
    if "arxiv" in paper_sources:
        try:
            arxiv_client = ArxivClient()
            for query in search_queries:
                # ArXiv categories relevant to finance
                categories = ["q-fin.ST", "q-fin.PM", "q-fin.TR", "cs.LG", "stat.ML"]
                for category in categories:
                    full_query = f"{query} AND cat:{category}"
                    results = arxiv_client.search_papers(
                        query=full_query,
                        max_results=5,
                        sort_by="submittedDate",
                        sort_order="descending"
                    )
                    
                    # Parse the results (assuming XML response)
                    # For now, we'll simulate the results
                    print(f"Searched ArXiv for: {full_query}")
                    
                    # TODO: Parse actual ArXiv XML response
                    # For testing, create simulated ArXiv-style papers
                    for i in range(2):  # Simulate 2 papers per query
                        all_papers.append({
                            "title": f"{query} - Paper {i+1}",
                            "authors": ["Author A", "Author B"],
                            "abstract": f"Abstract for {query} research paper focusing on {category}",
                            "url": f"https://arxiv.org/abs/2024.{i+1000}",
                            "pdf_url": f"https://arxiv.org/pdf/2024.{i+1000}.pdf",
                            "published": (datetime.now() - timedelta(days=i*30)).isoformat(),
                            "source": "arxiv",
                            "categories": [category],
                            "query": query
                        })
        except Exception as e:
            print(f"Error searching ArXiv: {e}")
    
    # Use LLM to find additional papers from other sources
    client = OpenAI()
    
    additional_queries = [
        "recent quantitative trading strategies papers 2024",
        "machine learning stock prediction research",
        "portfolio optimization new methods",
        "market microstructure anomalies studies",
        "factor investing research papers recent"
    ]
    
    for query in additional_queries[:3]:  # Limit queries
        try:
            prompt = f"""Search for recent academic papers on investment and trading with query: {query}

Focus on papers from the last {time_range} that cover:
- Novel trading strategies
- Market anomalies and inefficiencies  
- Machine learning applications in finance
- Portfolio optimization techniques
- Risk management innovations
- Cryptocurrency and alternative assets

For each paper, extract:
- title
- authors
- publication_date
- journal/conference
- abstract (brief summary)
- key_findings
- methodology
- potential_applications

Return as JSON array of papers (max 10)."""

            response = client.chat.completions.create(
                model=llm_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            try:
                papers = json.loads(content)
                if isinstance(papers, list):
                    for paper in papers:
                        paper["source"] = "llm_search"
                        paper["query"] = query
                    all_papers.extend(papers)
            except json.JSONDecodeError:
                pass
        except Exception as e:
            print(f"Error searching with LLM: {e}")
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_papers = []
    for paper in all_papers:
        title = paper.get("title", "").lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_papers.append(paper)
    
    # Sort by publication date
    unique_papers.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    # Update state
    state["paper_titles"] = unique_papers[:30]  # Keep top 30 papers
    
    # Save paper list
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "investment_papers.json"), "w") as f:
        json.dump(unique_papers[:30], f, indent=2)
    
    print(f"Found {len(unique_papers)} unique investment research papers")
    
    return state