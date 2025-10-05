"""
CoinGecko API service for price data and market information
"""
from typing import Dict, List, Optional, Any
from services.market_service import MarketService
from services.coin_service import CoinService

class CoinGeckoService(MarketService, CoinService):
    """Service for interacting with CoinGecko API"""
    
    def __init__(self):
        super().__init__()
    
    def get_supported_vs_currencies(self) -> Optional[List[str]]:
        """Get list of supported vs currencies"""
        url = f"{self.api_base}/simple/supported_vs_currencies"
        return self._make_request(url)
