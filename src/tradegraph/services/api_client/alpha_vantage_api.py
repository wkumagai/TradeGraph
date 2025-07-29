"""Alpha Vantage API client for stock market data."""

import os
import json
import time
from typing import Dict, Any, Optional
import urllib.request
import urllib.parse
from datetime import datetime


class AlphaVantageClient:
    """Client for Alpha Vantage API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Alpha Vantage client.
        
        Args:
            api_key: Alpha Vantage API key. If not provided, will look for
                    ALPHAVANTAGE_API_KEY in environment variables.
        """
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Alpha Vantage API key is required")
        
        self.base_url = "https://www.alphavantage.co/query"
        self.last_call_time = 0
        self.min_call_interval = 12  # seconds between calls for free tier
    
    def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Make a request to the Alpha Vantage API.
        
        Args:
            params: Query parameters for the API call
            
        Returns:
            JSON response as a dictionary
        """
        # Add API key to params
        params["apikey"] = self.api_key
        
        # Rate limiting
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        if time_since_last_call < self.min_call_interval:
            time.sleep(self.min_call_interval - time_since_last_call)
        
        # Build URL
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            self.last_call_time = time.time()
            
            # Check for API errors
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
            if "Note" in data:
                raise ValueError(f"API Note: {data['Note']}")
            
            return data
            
        except Exception as e:
            raise Exception(f"Alpha Vantage API request failed: {e}")
    
    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get real-time quote for a stock symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Quote data dictionary or None if not found
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol
        }
        
        data = self._make_request(params)
        
        if "Global Quote" in data:
            return data["Global Quote"]
        return None
    
    def get_daily_prices(self, symbol: str, outputsize: str = "compact") -> Optional[Dict[str, Any]]:
        """Get daily price data for a stock symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            outputsize: 'compact' (last 100 days) or 'full' (20+ years)
            
        Returns:
            Time series data or None if not found
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize
        }
        
        data = self._make_request(params)
        
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        return None
    
    def get_intraday_prices(self, symbol: str, interval: str = "5min") -> Optional[Dict[str, Any]]:
        """Get intraday price data for a stock symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            
        Returns:
            Time series data or None if not found
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval
        }
        
        data = self._make_request(params)
        
        time_series_key = f"Time Series ({interval})"
        if time_series_key in data:
            return data[time_series_key]
        return None
    
    def get_technical_indicator(self, symbol: str, indicator: str, 
                               interval: str = "daily", time_period: int = 20) -> Optional[Dict[str, Any]]:
        """Get technical indicator data for a stock.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            indicator: Technical indicator (e.g., 'RSI', 'MACD', 'SMA', 'EMA')
            interval: Time interval
            time_period: Number of data points used to calculate the indicator
            
        Returns:
            Technical indicator data or None if not found
        """
        params = {
            "function": indicator.upper(),
            "symbol": symbol,
            "interval": interval,
            "time_period": str(time_period),
            "series_type": "close"
        }
        
        data = self._make_request(params)
        
        # Find the technical analysis key in the response
        for key in data:
            if "Technical Analysis" in key:
                return data[key]
        return None