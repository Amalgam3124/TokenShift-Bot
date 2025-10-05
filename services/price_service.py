"""
Price service - Price data service
"""
import requests
from typing import Dict, List, Optional, Any
from config import Config

class PriceService:
    """Base class for price data service"""
    
    def __init__(self):
        self.api_base = Config.COINGECKO_API_BASE
        self.api_key = Config.COINGECKO_API_KEY
        self.headers = {}
        if self.api_key:
            self.headers['x-cg-demo-api-key'] = self.api_key
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make API request"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None
