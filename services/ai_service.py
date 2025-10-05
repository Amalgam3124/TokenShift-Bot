"""
OpenRouter AI service for token analysis
"""
import requests
import json
from typing import Dict, List, Optional, Any
from config import Config

class AIService:
    """Service for AI-powered token analysis using OpenRouter"""
    
    def __init__(self):
        self.api_base = Config.OPENROUTER_API_BASE
        self.api_key = Config.OPENROUTER_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://tokenshift-bot.com',
            'X-Title': 'TokenShift Bot'
        }
    
    def analyze_token(self, token_symbol: str) -> Optional[str]:
        """Simple token analysis for testing"""
        prompt = f"""
As a professional cryptocurrency analyst, please provide a brief analysis of {token_symbol.upper()} token:

Please provide:
1. Basic technical analysis
2. Short-term investment advice
3. Risk level assessment
4. Buy/Hold/Sell recommendations

Please respond in English, keeping it concise and professional.
"""
        
        return self._call_openrouter_api(prompt)
    
    def analyze_token_trends(self, token_data: Dict, timeframes: List[str] = ['1d', '3d', '1w', '1m']) -> Optional[str]:
        """Analyze token trends and provide investment advice"""
        
        # Prepare analysis prompt
        prompt = self._create_analysis_prompt(token_data, timeframes)
        
        # Call OpenRouter API
        response = self._call_openrouter_api(prompt)
        
        return response
    
    def _create_analysis_prompt(self, token_data: Dict, timeframes: List[str]) -> str:
        """Create analysis prompt for AI"""
        
        prompt = f"""
As a professional cryptocurrency analyst, please analyze based on the following real data:

Token Information:
- Name: {token_data.get('name', 'N/A')}
- Symbol: {token_data.get('symbol', 'N/A')}
- Current Price: ${token_data.get('current_price', 0):.6f}
- 24h Change: {token_data.get('price_change_percentage_24h', 0):.2f}%
- Market Cap: ${token_data.get('market_cap', 0):,.0f}
- 24h Volume: ${token_data.get('total_volume', 0):,.0f}

Technical Indicators:
- RSI (14): {token_data.get('rsi', 'N/A')}
- MACD: {token_data.get('macd', {}).get('macd', 'N/A')}
- MACD Signal: {token_data.get('macd', {}).get('signal', 'N/A')}
- MACD Histogram: {token_data.get('macd', {}).get('histogram', 'N/A')}
- Support Level: ${token_data.get('support_level', 'N/A')}
- Resistance Level: ${token_data.get('resistance_level', 'N/A')}
- Current Trend: {token_data.get('trend', 'N/A')}

Bollinger Bands:
- Upper: ${token_data.get('bollinger_bands', {}).get('upper', 'N/A')}
- Middle: ${token_data.get('bollinger_bands', {}).get('middle', 'N/A')}
- Lower: ${token_data.get('bollinger_bands', {}).get('lower', 'N/A')}

Timeframe Analysis:
"""
        
        for timeframe in timeframes:
            if timeframe in token_data.get('price_changes', {}):
                change = token_data['price_changes'][timeframe]
                prompt += f"- {timeframe}: {change:.2f}%\n"
        
        prompt += """

Please provide a professional analysis report based on the above real technical indicator data:

1. Technical Analysis Summary:
   - Comprehensive analysis based on RSI, MACD, Bollinger Bands and other indicators
   - Current price position relative to support and resistance levels
   - Trend strength and direction assessment

2. Multi-timeframe Analysis:
   - Short-term (1 day), medium-term (3 days-1 week), long-term (1 month) trends
   - Buy/sell signal strength across timeframes

3. Key Price Level Analysis:
   - Support and resistance level effectiveness
   - Bollinger Bands position analysis
   - Breakout probability assessment

4. Trading Signals:
   - Buy/sell signals based on MACD and RSI
   - Entry and exit timing recommendations
   - Stop-loss and take-profit level suggestions

5. Risk Level Assessment (1-10):
   - Technical risk
   - Market risk
   - Liquidity risk

6. Investment Recommendations:
   - Suitable investor types
   - Position management suggestions
   - Risk control measures

Please respond in English, keeping it professional, objective and practical.
"""
        
        return prompt
    
    def _call_openrouter_api(self, prompt: str) -> Optional[str]:
        """Call OpenRouter API for analysis"""
        
        url = f"{self.api_base}/chat/completions"
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                        "content": "You are a professional cryptocurrency analyst with extensive market experience and deep technical analysis capabilities. Please provide objective and professional analysis based on the provided data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            return None
    
    def generate_portfolio_analysis(self, portfolio_data: List[Dict]) -> Optional[str]:
        """Generate portfolio analysis"""
        
        prompt = f"""
As a professional portfolio analyst, please analyze the following portfolio:

Portfolio Data:
"""
        
        total_value = 0
        for asset in portfolio_data:
            value = asset.get('amount', 0) * asset.get('current_price', 0)
            total_value += value
            prompt += f"- {asset.get('token_symbol', 'N/A')}: {asset.get('amount', 0):.6f} (Value: ${value:.2f})\n"
        
        prompt += f"Total Value: ${total_value:.2f}\n\n"
        
        prompt += """
Please provide:
1. Portfolio risk assessment
2. Asset allocation recommendations
3. Positions that need adjustment
4. Overall investment strategy recommendations
5. Risk diversification suggestions

Please respond in English, keeping it professional and objective.
"""
        
        return self._call_openrouter_api(prompt)
    
    def get_market_sentiment(self, market_data: Dict) -> Optional[str]:
        """Analyze market sentiment"""
        
        prompt = f"""
As a market sentiment analyst, please analyze the current cryptocurrency market sentiment:

Market Data:
- Fear & Greed Index: {market_data.get('fear_greed_index', 'N/A')}
- Total Market Cap Change: {market_data.get('total_market_cap_change', 0):.2f}%
- Bitcoin Dominance: {market_data.get('btc_dominance', 0):.2f}%
- Active Addresses: {market_data.get('active_addresses', 'N/A')}
- Volume Change: {market_data.get('volume_change', 0):.2f}%

Please provide:
1. Current market sentiment assessment
2. Major trend analysis
3. Investment opportunity identification
4. Risk warnings
5. Market predictions

Please respond in English, keeping it professional and objective.
"""
        
        return self._call_openrouter_api(prompt)
