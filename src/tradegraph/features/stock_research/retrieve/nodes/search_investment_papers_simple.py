"""Simplified node for searching investment research papers."""

import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from openai import OpenAI


def search_investment_papers_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Search for investment research papers - simplified version for testing."""
    search_queries = state.get("search_queries", [])
    time_range = state.get("time_range", "1y")
    paper_sources = state.get("paper_sources", ["arxiv", "ssrn"])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    # Calculate date range
    time_map = {"1m": 30, "3m": 90, "6m": 180, "1y": 365, "2y": 730}
    days = time_map.get(time_range, 365)
    
    print("Generating simulated investment papers for testing...")
    
    # Generate simulated papers
    all_papers = []
    
    # Simulated ArXiv-style papers
    arxiv_templates = [
        {
            "title": "Deep Reinforcement Learning for Portfolio Optimization",
            "abstract": "We propose a novel deep reinforcement learning approach for dynamic portfolio optimization that adapts to changing market conditions.",
            "categories": ["q-fin.PM", "cs.LG"]
        },
        {
            "title": "Transformer Networks for Stock Price Prediction",
            "abstract": "This paper introduces a transformer-based architecture for predicting stock prices using attention mechanisms on financial time series data.",
            "categories": ["q-fin.ST", "cs.LG"]
        },
        {
            "title": "Market Anomaly Detection Using Graph Neural Networks",
            "abstract": "We present a graph neural network approach to detect market anomalies by modeling stock correlations as dynamic graphs.",
            "categories": ["q-fin.TR", "cs.LG"]
        },
        {
            "title": "High-Frequency Trading Strategies with Machine Learning",
            "abstract": "This study explores machine learning techniques for developing profitable high-frequency trading strategies in liquid markets.",
            "categories": ["q-fin.TR", "stat.ML"]
        },
        {
            "title": "Factor Investing with Alternative Data Sources",
            "abstract": "We investigate the use of alternative data sources including satellite imagery and social media sentiment for factor-based investing.",
            "categories": ["q-fin.PM", "q-fin.ST"]
        }
    ]
    
    # Add simulated papers
    for i, template in enumerate(arxiv_templates):
        paper_date = datetime.now() - timedelta(days=i*30)
        all_papers.append({
            "title": template["title"],
            "authors": [f"Author {j+1}" for j in range(3)],
            "abstract": template["abstract"],
            "url": f"https://arxiv.org/abs/2024.{1000+i}",
            "pdf_url": f"https://arxiv.org/pdf/2024.{1000+i}.pdf",
            "published": paper_date.isoformat(),
            "source": "arxiv",
            "categories": template["categories"],
            "query": search_queries[0] if search_queries else "investment research"
        })
    
    # Use LLM to generate additional papers
    client = OpenAI()
    
    prompt = f"""Generate 5 realistic academic paper titles and abstracts for investment/trading research.
    
    Focus on:
    - Machine learning for trading
    - Portfolio optimization
    - Market anomaly detection
    - Risk management
    - Alternative data sources
    
    For each paper provide:
    {{
        "title": "Paper title",
        "authors": ["Author 1", "Author 2"],
        "abstract": "2-3 sentence abstract",
        "journal": "Journal name or conference",
        "key_findings": "Main contribution",
        "methodology": "Brief method description"
    }}
    
    Return ONLY a JSON array."""
    
    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        papers = json.loads(content)
        if isinstance(papers, list):
            for paper in papers:
                paper["source"] = "llm_search"
                paper["published"] = (datetime.now() - timedelta(days=len(all_papers)*15)).isoformat()
                paper["url"] = f"https://example.com/paper/{len(all_papers)+1}"
                all_papers.append(paper)
    except Exception as e:
        print(f"Error generating papers with LLM: {e}")
    
    # Update state
    state["paper_titles"] = all_papers[:20]  # Keep top 20 papers
    
    # Save paper list
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "investment_papers.json"), "w") as f:
        json.dump(all_papers[:20], f, indent=2)
    
    print(f"Generated {len(all_papers)} simulated investment research papers")
    print("\nNOTE: This is simulated data for testing.")
    print("For production, implement real ArXiv API integration.")
    
    return state