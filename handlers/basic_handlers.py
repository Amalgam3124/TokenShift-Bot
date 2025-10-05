"""
Basic command handlers - Basic command handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from database.models import DatabaseManager

class BasicHandlers:
    """Handle basic commands"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Add user to database
        self.db.add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        welcome_message = f"""🚀 Welcome to TokenShift Bot!

Hello {user.first_name}! I'm your cryptocurrency trading assistant.

Available commands:
/daily - View today's top gaining tokens
/analysis <token> - AI analysis of token trends
/buy <token> <amount> - Buy tokens
/sellc <token> <amount> - Sell to USDC
/sellt <token> <amount> - Sell to USDT
/swap <token1> <amount> <token2> - Get token swap quote
/checkout - Execute pending swap
/wallet - Manage wallet
/delete - Delete bound wallet
/balance - Check balance

Getting started:
1. Use /wallet <private_key> to bind your wallet
2. Use /daily to view trending tokens
3. Use /analysis to get AI investment advice

⚠️ Investment involves risk, please make decisions carefully!"""
        
        await update.message.reply_text(welcome_message)
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """📚 TokenShift Bot Help

Main features:
• 📈 Real-time market data and analysis
• 🤖 AI-powered investment advice
• 💱 Secure token swapping
• 💼 Portfolio management
• 🔑 Secure wallet management

Command list:
/daily - View today's top gaining tokens
/analysis <token> - AI analysis of token trends
/buy <token> <amount> - Buy tokens
/sellc <token> <amount> - Sell to USDC
/sellt <token> <amount> - Sell to USDT
/swap <token1> <amount> <token2> - Get token swap quote
/checkout - Execute pending swap
/wallet - Manage wallet
/delete - Delete bound wallet
/balance - Check balance

Supported networks:
Ethereum, Arbitrum, Polygon, BSC, Avalanche, Optimism

Security tips:
• Private keys are encrypted and stored
• All transactions are securely verified
• Recommend using hardware wallets

For questions, please contact technical support."""
        
        await update.message.reply_text(help_message)
