"""Node for preparing datasets for backtesting."""

import os
import json
from typing import Dict, Any
from openai import OpenAI


def prepare_datasets_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare dataset specifications for the trading strategy backtest.
    
    This node defines data requirements, sources, and preprocessing steps.
    """
    trading_strategy = state.get("trading_strategy", {})
    experiment_design = state.get("experiment_design", {})
    llm_name = state.get("llm_name", "gpt-4o-mini-2024-07-18")
    
    client = OpenAI()
    
    prompt = f"""Define comprehensive dataset requirements for this trading strategy backtest.

Trading Strategy:
{json.dumps(trading_strategy, indent=2)}

Experiment Design:
{json.dumps(experiment_design, indent=2)}

Create dataset specifications with:

{{
  "primary_data": {{
    "price_data": {{
      "source": "yfinance/alpha_vantage/polygon/quandl",
      "frequency": "daily/hourly/minute",
      "fields": ["open", "high", "low", "close", "volume", "adjusted_close"],
      "universe": {{
        "method": "S&P500 constituents/Russell 3000/custom list",
        "point_in_time": true,
        "survivorship_bias_free": true
      }},
      "date_range": {{
        "start": "YYYY-MM-DD",
        "end": "YYYY-MM-DD",
        "timezone": "US/Eastern"
      }}
    }},
    "fundamental_data": {{
      "required": true/false,
      "source": "SimFin/Quandl/SEC filings",
      "fields": ["PE", "PB", "ROE", "Revenue", "EPS"],
      "frequency": "quarterly/annual"
    }}
  }},
  "alternative_data": {{
    "sentiment_data": {{
      "required": true/false,
      "source": "news/social media/analyst reports",
      "processing": "NLP sentiment scores"
    }},
    "macro_data": {{
      "required": true/false,
      "indicators": ["VIX", "DXY", "10Y yield", "Fed Funds Rate"],
      "source": "FRED/Yahoo Finance"
    }}
  }},
  "data_preprocessing": {{
    "cleaning": [
      "Remove outliers (>5 std dev)",
      "Handle missing data (forward fill/interpolate)",
      "Adjust for splits and dividends",
      "Remove stocks with <$1 price"
    ],
    "feature_engineering": [
      {{
        "name": "returns",
        "calculation": "(close - close.shift(1)) / close.shift(1)"
      }},
      {{
        "name": "volatility",
        "calculation": "returns.rolling(20).std()"
      }},
      {{
        "name": "rsi",
        "calculation": "ta.RSI(close, timeperiod=14)"
      }}
    ],
    "normalization": {{
      "price_data": "No normalization (use returns)",
      "volume_data": "Z-score normalization by stock",
      "fundamentals": "Cross-sectional rank normalization"
    }}
  }},
  "data_quality_checks": [
    {{
      "check": "Missing data percentage",
      "threshold": "< 5% per stock",
      "action": "Remove stocks exceeding threshold"
    }},
    {{
      "check": "Price continuity",
      "test": "No jumps > 50% in single day",
      "action": "Flag for manual review"
    }},
    {{
      "check": "Volume validation",
      "test": "Volume > 0 for tradable days",
      "action": "Mark as non-tradable if zero volume"
    }}
  ],
  "storage_format": {{
    "format": "parquet/csv/hdf5",
    "structure": "One file per date/One file per symbol/Single file",
    "compression": "snappy/gzip/none"
  }},
  "data_pipeline": {{
    "download_script": "Python script using yfinance + pandas",
    "update_frequency": "Daily after market close",
    "error_handling": "Retry failed downloads, log errors",
    "validation": "Compare against multiple sources"
  }},
  "estimated_size": {{
    "raw_data": "~X GB",
    "processed_data": "~Y GB",
    "features": "~Z GB"
  }},
  "data_dictionary": {{
    "price_fields": {{"field": "description"}},
    "calculated_features": {{"feature": "formula and description"}},
    "metadata": {{"field": "description"}}
  }}
}}

Ensure data requirements match the strategy's needs and experiment design."""

    try:
        response = client.chat.completions.create(
            model=llm_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        content = response.choices[0].message.content
        response = content
        # Try to parse as JSON
        try:
            dataset_specification = json.loads(response)
        except json.JSONDecodeError:
            dataset_specification = {
                "description": response,
                "primary_data": {"source": "yfinance", "frequency": "daily"}
            }
    except Exception as e:
        print(f"Error preparing datasets: {e}")
        dataset_specification = {"error": str(e)}
    
    # Save dataset specification
    save_dir = state.get("save_dir", "./stock_research_output")
    with open(os.path.join(save_dir, "experiment", "dataset_specification.json"), "w") as f:
        json.dump(dataset_specification, f, indent=2)
    
    # Update state
    state["dataset_specification"] = dataset_specification
    
    print("Dataset specifications prepared")
    
    return state