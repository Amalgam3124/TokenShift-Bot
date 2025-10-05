"""
Market service - Market data service
"""
from typing import Dict, List, Optional, Any
from services.price_service import PriceService

class MarketService(PriceService):
    """Market data service"""
    
    def get_trending_coins(self) -> Optional[List[Dict]]:
        """Get trending coins"""
        url = f"{self.api_base}/search/trending"
        data = self._make_request(url)
        return data.get('coins', []) if data else None
    
    def get_top_gainers(self, vs_currency: str = 'usd', days: int = 1) -> Optional[List[Dict]]:
        """Get top gaining coins"""
        url = f"{self.api_base}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': 'price_change_percentage_24h_desc',
            'per_page': 50,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': f'{days}d'
        }
        return self._make_request(url, params)
    
    def get_market_cap_global(self) -> Optional[Dict]:
        """Get global market cap data"""
        url = f"{self.api_base}/global"
        return self._make_request(url)
