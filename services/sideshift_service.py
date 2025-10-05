"""
SideShift.ai API service for token swapping
"""
from typing import Dict, List, Optional, Any
from services.swap_service import SwapService
from services.coin_info_service import CoinInfoService

class SideShiftService(SwapService, CoinInfoService):
    """Service for interacting with SideShift.ai API"""
    
    def __init__(self):
        super().__init__()
    
    def swap_tokens(self, from_token: str, to_token: str, amount: str, 
                   from_network: str, to_network: str, user_address: str) -> Optional[Dict]:
        """Execute token swap"""
        # First get a quote
        quote = self.get_quote(
            deposit_coin=from_token,
            deposit_network=from_network,
            settle_coin=to_token,
            settle_network=to_network,
            deposit_amount=amount
        )
        
        if not quote:
            return None
        
        # Create the shift
        shift = self.create_fixed_shift(quote['id'], user_address)
        return shift
    
    def create_checkout_session(self, settle_coin: str, settle_network: str, settle_amount: str, 
                               settle_address: str, success_url: str = None, cancel_url: str = None) -> Optional[Dict]:
        """Create a checkout session for easy token purchase"""
        return self.create_checkout(
            settle_coin=settle_coin,
            settle_network=settle_network,
            settle_amount=settle_amount,
            settle_address=settle_address,
            success_url=success_url,
            cancel_url=cancel_url
        )
    
