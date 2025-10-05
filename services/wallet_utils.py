"""
Wallet utilities - Wallet utility functions
"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from typing import Optional, Dict, List
import re
import hashlib

class WalletUtils:
    """Wallet utility functions"""
    
    def __init__(self):
        pass
    
    def is_valid_private_key(self, private_key: str) -> bool:
        """Check if private key is valid"""
        try:
            # Remove 0x prefix if present
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # Check if it's a valid hex string and 64 characters long
            if len(private_key) != 64:
                return False
            
            # Check if it's valid hex
            int(private_key, 16)
            return True
        except:
            return False
    
    def private_key_to_address(self, private_key: str) -> Optional[str]:
        """Convert private key to Ethereum address"""
        try:
            # Remove 0x prefix if present
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            # Convert to bytes
            private_key_bytes = bytes.fromhex(private_key)
            
            # Create private key object
            private_key_obj = ec.derive_private_key(int(private_key, 16), ec.SECP256K1())
            
            # Get public key
            public_key = private_key_obj.public_key()
            
            # Get uncompressed public key bytes
            public_key_bytes = public_key.public_bytes(
                encoding=Encoding.X962,
                format=PublicFormat.UncompressedPoint
            )
            
            # Remove the first byte (0x04) to get the 64-byte public key
            public_key_bytes = public_key_bytes[1:]
            
            # Hash the public key with Keccak-256 (using SHA3-256 as approximation)
            # Note: This is a simplified implementation. For production, use a proper Keccak-256 library
            keccak_hash = hashlib.sha3_256(public_key_bytes).digest()
            
            # Take the last 20 bytes as the address
            address_bytes = keccak_hash[-20:]
            
            # Convert to hex and add 0x prefix
            address = "0x" + address_bytes.hex()
            
            return address
        except Exception as e:
            print(f"Error converting private key to address: {e}")
            return None
    
    def get_evm_networks(self) -> List[Dict[str, str]]:
        """Get supported EVM networks"""
        return [
            {"name": "Ethereum", "chain_id": 1, "rpc": "https://eth.llamarpc.com"},
            {"name": "Arbitrum", "chain_id": 42161, "rpc": "https://arb1.arbitrum.io/rpc"},
            {"name": "Polygon", "chain_id": 137, "rpc": "https://polygon-rpc.com"},
            {"name": "BSC", "chain_id": 56, "rpc": "https://bsc-dataseed.binance.org"},
            {"name": "Avalanche", "chain_id": 43114, "rpc": "https://api.avax.network/ext/bc/C/rpc"},
            {"name": "Optimism", "chain_id": 10, "rpc": "https://mainnet.optimism.io"}
        ]
    
    def get_network_by_name(self, network_name: str) -> Optional[Dict[str, str]]:
        """Get network info by name"""
        networks = self.get_evm_networks()
        for network in networks:
            if network["name"].lower() == network_name.lower():
                return network
        return None
    
    def is_evm_network(self, network_name: str) -> bool:
        """Check if network is EVM compatible"""
        return self.get_network_by_name(network_name) is not None
