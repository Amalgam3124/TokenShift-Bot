"""
Coin service - Token data service
"""
from typing import Dict, List, Optional, Any
from services.price_service import PriceService

class CoinService(PriceService):
    """Token data service"""
    
    def get_coin_price(self, coin_id: str, vs_currencies: str = 'usd') -> Optional[Dict]:
        """Get current price of a coin"""
        url = f"{self.api_base}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': vs_currencies,
            'include_24hr_change': True,
            'include_24hr_vol': True,
            'include_market_cap': True
        }
        return self._make_request(url, params)
    
    def get_coin_market_chart(self, coin_id: str, vs_currency: str = 'usd', 
                            days: int = 1) -> Optional[Dict]:
        """Get market chart data for a coin"""
        url = f"{self.api_base}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days,
            'interval': 'hourly' if days <= 1 else 'daily'
        }
        return self._make_request(url, params)
    
    def search_coins(self, query: str) -> Optional[List[Dict]]:
        """Search for coins by name or symbol"""
        url = f"{self.api_base}/search"
        params = {'query': query}
        data = self._make_request(url, params)
        return data.get('coins', []) if data else None
    
    def get_coin_info(self, coin_id: str) -> Optional[Dict]:
        """Get detailed information about a coin"""
        url = f"{self.api_base}/coins/{coin_id}"
        params = {
            'localization': False,
            'tickers': False,
            'market_data': True,
            'community_data': False,
            'developer_data': False,
            'sparkline': False
        }
        return self._make_request(url, params)
