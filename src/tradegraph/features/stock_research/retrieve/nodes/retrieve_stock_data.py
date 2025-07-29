"""Node for retrieving real stock market data using Alpha Vantage API."""

import os
import json
import requests
from typing import Dict, Any, List
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def retrieve_stock_data_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve real stock market data using Alpha Vantage API.
    
    This node fetches real-time and historical stock data for analysis.
    """
    stock_symbols = state.get("stock_symbols", [])
    data_types = state.get("data_types", ["quote", "daily"])
    save_dir = state.get("save_dir", "./stock_research_output")
    
    # Get API key from environment
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        print("ERROR: ALPHAVANTAGE_API_KEY not found in environment variables")
        state["market_data"] = {}
        return state
    
    print(f"Using Alpha Vantage API to fetch real stock data...")
    
    all_data = {}
    base_url = "https://www.alphavantage.co/query"
    
    for symbol in stock_symbols[:5]:  # Limit to 5 to avoid API rate limits
        symbol_data = {}
        
        # Fetch real-time quote data
        if "quote" in data_types:
            try:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": api_key
                }
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if "Global Quote" in data:
                        quote = data["Global Quote"]
                        symbol_data["quote"] = {
                            "symbol": quote.get("01. symbol", symbol),
                            "price": float(quote.get("05. price", 0)),
                            "change": float(quote.get("09. change", 0)),
                            "change_percent": quote.get("10. change percent", "0%"),
                            "volume": int(quote.get("06. volume", 0)),
                            "latest_trading_day": quote.get("07. latest trading day"),
                            "previous_close": float(quote.get("08. previous close", 0)),
                            "timestamp": datetime.now().isoformat()
                        }
                        print(f"✓ Retrieved quote for {symbol}: ${symbol_data['quote']['price']}")
                    else:
                        print(f"⚠️  No quote data available for {symbol}")
                else:
                    print(f"❌ Failed to fetch quote for {symbol}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error fetching quote for {symbol}: {e}")
        
        # Fetch daily time series data
        if "daily" in data_types:
            try:
                params = {
                    "function": "TIME_SERIES_DAILY",
                    "symbol": symbol,
                    "apikey": api_key,
                    "outputsize": "compact"  # Last 100 days
                }
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if "Time Series (Daily)" in data:
                        time_series = data["Time Series (Daily)"]
                        # Convert to more usable format
                        daily_data = []
                        for date, values in sorted(time_series.items(), reverse=True)[:30]:  # Last 30 days
                            daily_data.append({
                                "date": date,
                                "open": float(values["1. open"]),
                                "high": float(values["2. high"]),
                                "low": float(values["3. low"]),
                                "close": float(values["4. close"]),
                                "volume": int(values["5. volume"])
                            })
                        symbol_data["daily"] = daily_data
                        print(f"✓ Retrieved {len(daily_data)} days of data for {symbol}")
                    else:
                        print(f"⚠️  No daily data available for {symbol}")
                else:
                    print(f"❌ Failed to fetch daily data for {symbol}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error fetching daily data for {symbol}: {e}")
        
        # Fetch technical indicators
        if "indicators" in data_types:
            # RSI (Relative Strength Index)
            try:
                params = {
                    "function": "RSI",
                    "symbol": symbol,
                    "interval": "daily",
                    "time_period": 14,
                    "series_type": "close",
                    "apikey": api_key
                }
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if "Technical Analysis: RSI" in data:
                        rsi_data = data["Technical Analysis: RSI"]
                        # Get latest RSI values
                        latest_rsi = []
                        for date, values in sorted(rsi_data.items(), reverse=True)[:10]:
                            latest_rsi.append({
                                "date": date,
                                "rsi": float(values["RSI"])
                            })
                        symbol_data["rsi"] = latest_rsi
                        print(f"✓ Retrieved RSI data for {symbol}")
                else:
                    print(f"⚠️  Could not fetch RSI for {symbol}")
            except Exception as e:
                print(f"❌ Error fetching RSI for {symbol}: {e}")
        
        all_data[symbol] = symbol_data
    
    # Calculate some basic statistics
    market_summary = {
        "timestamp": datetime.now().isoformat(),
        "symbols_analyzed": len(all_data),
        "market_overview": {}
    }
    
    # Analyze market trends
    gainers = []
    losers = []
    
    for symbol, data in all_data.items():
        if "quote" in data:
            quote = data["quote"]
            change_pct = float(quote["change_percent"].rstrip("%"))
            
            if change_pct > 0:
                gainers.append({
                    "symbol": symbol,
                    "price": quote["price"],
                    "change_percent": change_pct
                })
            else:
                losers.append({
                    "symbol": symbol,
                    "price": quote["price"],
                    "change_percent": change_pct
                })
    
    market_summary["market_overview"] = {
        "top_gainers": sorted(gainers, key=lambda x: x["change_percent"], reverse=True)[:3],
        "top_losers": sorted(losers, key=lambda x: x["change_percent"])[:3],
        "average_change": sum(g["change_percent"] for g in gainers + losers) / len(gainers + losers) if gainers + losers else 0
    }
    
    # Update state
    state["market_data"] = all_data
    state["market_summary"] = market_summary
    
    # Save market data
    os.makedirs(save_dir, exist_ok=True)
    
    with open(os.path.join(save_dir, "market_data.json"), "w") as f:
        json.dump(all_data, f, indent=2)
    
    with open(os.path.join(save_dir, "market_summary.json"), "w") as f:
        json.dump(market_summary, f, indent=2)
    
    print(f"\n📊 Market Summary:")
    print(f"  - Symbols analyzed: {market_summary['symbols_analyzed']}")
    print(f"  - Average change: {market_summary['market_overview']['average_change']:.2f}%")
    print(f"  - Data saved to: {save_dir}")
    
    return state