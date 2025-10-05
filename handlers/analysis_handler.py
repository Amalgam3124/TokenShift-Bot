"""
Analysis command handler - AI analysis of token trends
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.coingecko_service import CoinGeckoService
from services.ai_service import AIService
from services.technical_analysis import TechnicalAnalysis

class AnalysisHandler:
    """Handle /analysis command"""
    
    def __init__(self):
        self.coingecko = CoinGeckoService()
        self.ai = AIService()
        self.technical = TechnicalAnalysis()
    
    async def handle_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analysis command - AI analysis of token trends"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❌ Please provide token symbol\n"
                    "Usage: /analysis <token_symbol>\n"
                    "Example: /analysis btc"
                )
                return
            
            token_symbol = context.args[0].upper()
            
            # Send loading message
            loading_msg = await update.message.reply_text("🔍 Fetching token data...")
            
            # Search for token in CoinGecko
            search_results = self.coingecko.search_coins(token_symbol)
            if not search_results:
                await loading_msg.edit_text(f"❌ Token not found: {token_symbol}")
                return
            
            # Get the first result
            coin_id = search_results[0]['id']
            coin_name = search_results[0]['name']
            
            await loading_msg.edit_text("📊 Fetching price data...")
            
            # Get detailed coin information
            coin_info = self.coingecko.get_coin_info(coin_id)
            if not coin_info:
                await loading_msg.edit_text(f"❌ Unable to get token info: {token_symbol}")
                return
            
            # Get market chart data for technical analysis (30 days)
            chart_data = self.coingecko.get_coin_market_chart(coin_id, days=30)
            if not chart_data or not chart_data.get('prices'):
                await loading_msg.edit_text(f"❌ Unable to get price chart data: {token_symbol}")
                return
            
            # Extract prices for technical analysis
            prices = [price[1] for price in chart_data['prices']]  # Extract price values
            
            # Calculate technical indicators
            await loading_msg.edit_text("📈 Calculating technical indicators...")
            technical_indicators = self.technical.get_technical_indicators(prices)
            
            # Get price changes for different timeframes
            market_data = {}
            timeframes = ['1d', '3d', '1w', '1m']
            
            for timeframe in timeframes:
                days = 1 if timeframe == '1d' else 3 if timeframe == '3d' else 7 if timeframe == '1w' else 30
                chart_data_tf = self.coingecko.get_coin_market_chart(coin_id, days=days)
                if chart_data_tf and chart_data_tf.get('prices'):
                    prices_tf = chart_data_tf['prices']
                    if len(prices_tf) >= 2:
                        start_price = prices_tf[0][1]
                        end_price = prices_tf[-1][1]
                        change = ((end_price - start_price) / start_price) * 100
                        market_data[timeframe] = change
            
            # Prepare comprehensive data for AI analysis
            analysis_data = {
                'name': coin_name,
                'symbol': token_symbol,
                'current_price': coin_info.get('market_data', {}).get('current_price', {}).get('usd', 0),
                'price_change_percentage_24h': coin_info.get('market_data', {}).get('price_change_percentage_24h', 0),
                'market_cap': coin_info.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                'total_volume': coin_info.get('market_data', {}).get('total_volume', {}).get('usd', 0),
                'price_changes': market_data,
                'rsi': technical_indicators['rsi'],
                'macd': technical_indicators['macd'],
                'support_level': technical_indicators['support_resistance']['support'],
                'resistance_level': technical_indicators['support_resistance']['resistance'],
                'bollinger_bands': technical_indicators['bollinger_bands'],
                'trend': technical_indicators['trend']
            }
            
            await loading_msg.edit_text("🤖 AI is analyzing token trends, please wait...")
            
            # Get AI analysis
            analysis = self.ai.analyze_token_trends(analysis_data)
            
            if not analysis:
                await loading_msg.edit_text("❌ AI analysis failed, please try again later")
                return
            
            # Send analysis result
            await loading_msg.edit_text(f"🤖 {token_symbol} AI Analysis Report\n\n{analysis}")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
