"""
Swap service - Token swap service
"""
import requests
from typing import Dict, List, Optional, Any
from config import Config

class SwapService:
    """Token swap service"""
    
    def __init__(self):
        self.api_base = Config.SIDESHIFT_API_BASE
        self.secret = Config.SIDESHIFT_SECRET
        self.affiliate_id = Config.SIDESHIFT_AFFILIATE_ID
        self.headers = {
            'Content-Type': 'application/json',
            'x-sideshift-secret': self.secret
        }
    
    def get_quote(self, deposit_coin: str, deposit_network: str, 
                  settle_coin: str, settle_network: str, 
                  deposit_amount: str = None, settle_amount: str = None) -> Optional[Dict]:
        """Get a quote for token swap"""
        url = f"{self.api_base}/quotes"
        data = {
            "depositCoin": deposit_coin,
            "depositNetwork": deposit_network,
            "settleCoin": settle_coin,
            "settleNetwork": settle_network,
            "affiliateId": self.affiliate_id
        }
        
        if deposit_amount:
            data["depositAmount"] = deposit_amount
        if settle_amount:
            data["settleAmount"] = settle_amount
            
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting quote: {e}")
            return None
    
    def create_fixed_shift(self, quote_id: str, settle_address: str, refund_address: str = None) -> Optional[Dict]:
        """Create a fixed shift"""
        url = f"{self.api_base}/shifts/fixed"
        data = {
            "quoteId": quote_id,
            "settleAddress": settle_address,
            "affiliateId": self.affiliate_id
        }
        
        # Add refund address if provided
        if refund_address:
            data["refundAddress"] = refund_address
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating shift: {e}")
            return None
    
    def get_shift_status(self, shift_id: str) -> Optional[Dict]:
        """Get shift status"""
        url = f"{self.api_base}/shifts/{shift_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting shift status: {e}")
            return None
    
    def create_checkout(self, settle_coin: str, settle_network: str, settle_amount: str, 
                       settle_address: str, success_url: str, cancel_url: str) -> Optional[Dict]:
        """Create a checkout session"""
        url = f"{self.api_base}/checkout"
        data = {
            "settleCoin": settle_coin,
            "settleNetwork": settle_network,
            "settleAmount": settle_amount,
            "settleAddress": settle_address,
            "affiliateId": self.affiliate_id,
            "successUrl": success_url,
            "cancelUrl": cancel_url
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-sideshift-secret': self.secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating checkout: {e}")
            return None
    
