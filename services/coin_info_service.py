"""
Coin info service - Token info service
"""
import requests
from typing import Dict, List, Optional, Any
from config import Config

class CoinInfoService:
    """Token info service"""
    
    def __init__(self):
        self.api_base = Config.SIDESHIFT_API_BASE
        self.secret = Config.SIDESHIFT_SECRET
        self.affiliate_id = Config.SIDESHIFT_AFFILIATE_ID
        self.headers = {
            'Content-Type': 'application/json',
            'x-sideshift-secret': self.secret
        }
    
    def get_supported_coins(self) -> Optional[Dict]:
        """Get list of supported coins"""
        url = f"{self.api_base}/coins"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Handle both list and dict responses
            if isinstance(data, list):
                return {"coins": data}
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error getting supported coins: {e}")
            return None
    
    def get_coin_info(self, coin: str) -> Optional[Dict]:
        """Get information about a specific coin"""
        url = f"{self.api_base}/coins/{coin}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting coin info: {e}")
            return None
    
    def get_coin_networks(self, coin: str) -> Optional[List[str]]:
        """Get supported networks for a coin"""
        coin_info = self.get_coin_info(coin)
        if coin_info and 'networks' in coin_info:
            return list(coin_info['networks'].keys())
        return None
