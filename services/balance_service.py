"""
Balance service - Query USDT/USDC balances across EVM networks
"""
import requests
import json
from typing import Dict, List, Optional, Any
from decimal import Decimal

class BalanceService:
    """Service for querying token balances across EVM networks"""
    
    def __init__(self):
        # Token contract addresses for different networks
        self.token_contracts = {
            'ethereum': {
                'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                'USDC': '0xA0b86a33E6441b8C4C8C0e4b8b8C8C0e4b8b8C8C0'
            },
            'arbitrum': {
                'USDT': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
                'USDC': '0xaf88d065e77c8cC2239327C5EDb3A432268e5831'
            },
            'polygon': {
                'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
                'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
            },
            'bsc': {
                'USDT': '0x55d398326f99059fF775485246999027B3197955',
                'USDC': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
            },
            'avalanche': {
                'USDT': '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
                'USDC': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E'
            },
            'optimism': {
                'USDT': '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58',
                'USDC': '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85'
            }
        }
        
        # RPC endpoints for different networks
        self.rpc_endpoints = {
            'ethereum': 'https://eth.llamarpc.com',
            'arbitrum': 'https://arb1.arbitrum.io/rpc',
            'polygon': 'https://polygon-rpc.com',
            'bsc': 'https://bsc-dataseed.binance.org',
            'avalanche': 'https://api.avax.network/ext/bc/C/rpc',
            'optimism': 'https://mainnet.optimism.io'
        }
    
    def get_token_balance(self, wallet_address: str, token_contract: str, network: str) -> Optional[Decimal]:
        """Get token balance for a specific contract"""
        try:
            rpc_url = self.rpc_endpoints.get(network)
            if not rpc_url:
                return None
            
            # ERC-20 balanceOf function call
            data = {
                "jsonrpc": "2.0",
                "method": "eth_call",
                "params": [
                    {
                        "to": token_contract,
                        "data": f"0x70a08231000000000000000000000000{wallet_address[2:].lower()}"
                    },
                    "latest"
                ],
                "id": 1
            }
            
            response = requests.post(rpc_url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and result['result'] != '0x':
                    # Convert hex to decimal
                    balance_hex = result['result']
                    balance_wei = int(balance_hex, 16)
                    # Convert from wei to token units (18 decimals for most tokens)
                    balance = Decimal(balance_wei) / Decimal(10**18)
                    return balance
            return None
            
        except Exception as e:
            print(f"Error getting balance for {network}: {e}")
            return None
    
    def get_eth_balance(self, wallet_address: str, network: str) -> Optional[Decimal]:
        """Get native ETH balance"""
        try:
            rpc_url = self.rpc_endpoints.get(network)
            if not rpc_url:
                return None
            
            data = {
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [wallet_address, "latest"],
                "id": 1
            }
            
            response = requests.post(rpc_url, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if 'result' in result:
                    balance_wei = int(result['result'], 16)
                    balance_eth = Decimal(balance_wei) / Decimal(10**18)
                    return balance_eth
            return None
            
        except Exception as e:
            print(f"Error getting ETH balance for {network}: {e}")
            return None
    
    def get_wallet_balances(self, wallet_address: str) -> Dict[str, Dict[str, Any]]:
        """Get all balances for a wallet across all networks"""
        balances = {}
        
        for network, tokens in self.token_contracts.items():
            network_balances = {
                'ETH': None,
                'USDT': None,
                'USDC': None
            }
            
            # Get ETH balance
            eth_balance = self.get_eth_balance(wallet_address, network)
            if eth_balance is not None:
                network_balances['ETH'] = float(eth_balance)
            
            # Get USDT balance
            usdt_contract = tokens.get('USDT')
            if usdt_contract:
                usdt_balance = self.get_token_balance(wallet_address, usdt_contract, network)
                if usdt_balance is not None:
                    network_balances['USDT'] = float(usdt_balance)
            
            # Get USDC balance
            usdc_contract = tokens.get('USDC')
            if usdc_contract:
                usdc_balance = self.get_token_balance(wallet_address, usdc_contract, network)
                if usdc_balance is not None:
                    network_balances['USDC'] = float(usdc_balance)
            
            # Include all networks (even with zero balances)
            balances[network] = network_balances
        
        return balances
    
    def format_balance_message(self, balances: Dict[str, Dict[str, Any]]) -> str:
        """Format balance data into a readable message"""
        if not balances:
            return "💰 **Balance Query**\n\n❌ No balances found or unable to query balances"
        
        message = "💰 **Balance Query**\n\n"
        
        for network, tokens in balances.items():
            network_name = network.capitalize()
            message += f"🌐 **{network_name}**\n"
            
            has_balance = False
            for token, balance in tokens.items():
                if balance is not None and balance > 0:
                    has_balance = True
                    if token == 'ETH':
                        message += f"  • ETH: {balance:.6f}\n"
                    else:
                        message += f"  • {token}: {balance:.2f}\n"
            
            if not has_balance:
                message += f"  • No balances found\n"
            
            message += "\n"
        
        return message
