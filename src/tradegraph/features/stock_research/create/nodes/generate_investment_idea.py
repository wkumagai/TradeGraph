"""Node for generating investment ideas."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def generate_investment_idea_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a novel investment idea based on market insights and research.
    
    This node creates innovative investment thesis by combining insights
    from news, research papers, and market conditions.
    """
    market_insights = state.get("market_insights", "")
    research_papers = state.get("research_papers", "")
    investment_goals = state.get("investment_goals", [])
    constraints = state.get("constraints", [])
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Generate a novel investment idea based on current market conditions and research.

Market Insights:
{market_insights}

Research Papers Summary:
{research_papers}

Investment Goals:
{json.dumps(investment_goals, indent=2)}

Constraints:
{json.dumps(constraints, indent=2)}

Create an innovative investment thesis that:

1. **Core Concept**: A clear, unique investment approach
   - What makes this different from existing strategies?
   - What market inefficiency does it exploit?
   - Why might this work now but not before?

2. **Theoretical Foundation**: 
   - Economic rationale
   - Behavioral finance aspects
   - Market microstructure considerations

3. **Target Assets**:
   - Specific asset classes or securities
   - Selection criteria
   - Universe definition

4. **Edge Source**:
   - Information advantage
   - Processing advantage
   - Behavioral advantage
   - Structural advantage

5. **Risk/Return Profile**:
   - Expected returns
   - Risk characteristics
   - Correlation with traditional strategies

6. **Implementation Feasibility**:
   - Data requirements
   - Computational needs
   - Trading frequency
   - Capital requirements

Be creative but realistic. Focus on strategies that could actually be implemented by individual investors or small funds.

Format as a detailed investment thesis document."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000
        )
        investment_idea = response.choices[0].message.content
    except Exception as e:
        print(f"Error generating investment idea: {e}")
        investment_idea = "Failed to generate investment idea."
    
    # Save the investment idea
    save_dir = state.get("save_dir", "./stock_research_output")
    os.makedirs(os.path.join(save_dir, "investment_method"), exist_ok=True)
    
    with open(os.path.join(save_dir, "investment_method", "investment_idea.md"), "w") as f:
        f.write(investment_idea)
    
    # Update state
    state["investment_idea"] = investment_idea
    
    print("Investment idea generated")
    
    return state