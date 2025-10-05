"""
Configuration module for TokenShift bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the bot"""
    
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # SideShift.ai API Configuration
    SIDESHIFT_SECRET = os.getenv('SIDESHIFT_SECRET')
    SIDESHIFT_AFFILIATE_ID = os.getenv('SIDESHIFT_AFFILIATE_ID')
    SIDESHIFT_API_BASE = 'https://sideshift.ai/api/v2'
    
    # Price Data APIs
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    COINGECKO_API_BASE = 'https://api.coingecko.com/api/v3'
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_API_BASE = os.getenv('OPENROUTER_API_BASE', 'https://openrouter.ai/api/v1')
    
    # Database Configuration
    DATABASE_PATH = 'tokenshift.db'
    
    # Supported networks for SideShift
    SUPPORTED_NETWORKS = {
        'ethereum': 'mainnet',
        'arbitrum': 'arbitrum',
        'polygon': 'polygon',
        'bsc': 'bsc',
        'avalanche': 'avalanche',
        'optimism': 'optimism'
    }
    
    # Supported stablecoins
    STABLECOINS = {
        'usdt': ['ethereum', 'arbitrum', 'polygon', 'bsc', 'avalanche', 'optimism'],
        'usdc': ['ethereum', 'arbitrum', 'polygon', 'bsc', 'avalanche', 'optimism']
    }
