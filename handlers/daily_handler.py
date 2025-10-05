"""
Daily command handler - Get top gaining tokens
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.coingecko_service import CoinGeckoService
from services.sideshift_service import SideShiftService

class DailyHandler:
    """Handle /daily command"""
    
    def __init__(self):
        self.coingecko = CoinGeckoService()
        self.sideshift = SideShiftService()
    
    async def handle_daily(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /daily command - show top gaining tokens"""
        try:
            await update.message.reply_text("Fetching market data...")
            
            # Get top gainers from CoinGecko
            gainers = self.coingecko.get_top_gainers()
            
            if not gainers:
                await update.message.reply_text("❌ Unable to fetch market data, please try again later")
                return
            
            # Get supported coins from SideShift
            supported_coins = self.sideshift.get_supported_coins()
            if not supported_coins:
                await update.message.reply_text("❌ Unable to fetch supported tokens list")
                return
            
            # Create mapping of supported symbols (use 'coin' field from SideShift)
            supported_symbols = set()
            for coin in supported_coins.get('coins', []):
                symbol = coin.get('coin', '').lower()
                if symbol:
                    supported_symbols.add(symbol)
            
            # Filter gainers to only include SideShift supported tokens
            filtered_gainers = []
            for coin in gainers:
                symbol = coin.get('symbol', '').lower()
                if symbol in supported_symbols:
                    filtered_gainers.append(coin)
            
            # Sort by 24h change percentage (descending)
            filtered_gainers.sort(key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)
            
            # Take top 10
            filtered_gainers = filtered_gainers[:10]
            
            if not filtered_gainers:
                await update.message.reply_text("❌ No SideShift supported gaining tokens found")
                return
            
            # Format message
            message = "📈 Today's Top Gaining Tokens\n\n"
            
            for i, coin in enumerate(filtered_gainers, 1):
                name = coin.get('name', 'N/A')
                symbol = coin.get('symbol', 'N/A')
                price = coin.get('current_price', 0)
                change_24h = coin.get('price_change_percentage_24h', 0)
                market_cap = coin.get('market_cap', 0)
                
                emoji = "🚀" if change_24h > 10 else "📈" if change_24h > 0 else "📉"
                
                message += f"{i}. {emoji} {name} ({symbol})\n"
                message += f"   Price: ${price:.6f}\n"
                message += f"   24h Change: {change_24h:+.2f}%\n"
                message += f"   Market Cap: ${market_cap:,.0f}\n\n"
            
            await update.message.reply_text(message)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
