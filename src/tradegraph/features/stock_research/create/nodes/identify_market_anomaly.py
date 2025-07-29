"""Node for identifying market anomalies to exploit."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def identify_market_anomaly_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Identify specific market anomalies or inefficiencies to exploit.
    
    This node analyzes the investment idea to pinpoint concrete market
    anomalies that can form the basis of a trading strategy.
    """
    investment_idea = state.get("investment_idea", "")
    market_insights = state.get("market_insights", "")
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Based on the investment idea, identify specific market anomalies or inefficiencies to exploit.

Investment Idea:
{investment_idea}

Current Market Insights:
{market_insights}

Identify and describe market anomalies in the following JSON structure:

{{
  "anomaly_name": "Descriptive name for the anomaly",
  "anomaly_type": "momentum/mean_reversion/sentiment/structural/behavioral/seasonal",
  "description": "Detailed description of the anomaly",
  "evidence": {{
    "empirical": "Historical evidence supporting this anomaly",
    "theoretical": "Academic or theoretical support",
    "recent_examples": ["Specific recent instances"]
  }},
  "exploitation_method": {{
    "signal_generation": "How to identify when anomaly is present",
    "entry_rules": "When to enter positions",
    "exit_rules": "When to exit positions",
    "position_sizing": "How to size positions"
  }},
  "market_conditions": {{
    "works_best": "Market conditions where anomaly is strongest",
    "fails_when": "Conditions where anomaly disappears",
    "regime_dependency": "How it varies with market regimes"
  }},
  "statistical_properties": {{
    "frequency": "How often the anomaly occurs",
    "magnitude": "Typical size of the opportunity",
    "persistence": "How long the anomaly lasts",
    "predictability": "How reliably it can be predicted"
  }},
  "risks": {{
    "crowding": "Risk of strategy becoming overcrowded",
    "regime_change": "Risk of anomaly disappearing",
    "execution": "Trading and implementation risks"
  }}
}}

Focus on anomalies that are:
1. Persistent enough to be exploitable
2. Large enough to overcome transaction costs
3. Not yet fully arbitraged away
4. Suitable for the stated constraints

Provide a detailed, actionable anomaly description."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        response_text = response.choices[0].message.content
        # Try to parse as JSON
        try:
            market_anomaly = json.loads(response_text)
        except json.JSONDecodeError:
            # If not valid JSON, create a structured dict from the text
            market_anomaly = {
                "anomaly_name": "Identified Anomaly",
                "description": response_text,
                "anomaly_type": "unknown",
                "exploitation_method": {
                    "signal_generation": "To be determined",
                    "entry_rules": "To be determined"
                }
            }
    except Exception as e:
        print(f"Error identifying anomaly: {e}")
        market_anomaly = {
            "anomaly_name": "Error",
            "description": "Failed to identify anomaly",
            "error": str(e)
        }
    
    # Save the anomaly analysis
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "investment_method", "market_anomaly.json"), "w") as f:
        json.dump(market_anomaly, f, indent=2)
    
    # Update state
    state["market_anomaly"] = market_anomaly
    
    print(f"Identified market anomaly: {market_anomaly.get('anomaly_name', 'Unknown')}")
    
    return state