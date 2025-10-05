"""
Message handlers for Telegram bot
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.ai_service import AIService
from database.models import DatabaseManager

class MessageHandlers:
    """Handlers for non-command messages"""
    
    def __init__(self):
        self.ai = AIService()
        self.db = DatabaseManager()
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        try:
            user_id = update.effective_user.id
            message_text = update.message.text.lower().strip()
            
            # Check for wallet deletion confirmation
            if context.user_data.get('pending_wallet_deletion', False):
                if message_text == 'confirm':
                    # Delete user's wallets
                    self.db.delete_user_wallets(user_id)
                    context.user_data['pending_wallet_deletion'] = False
                    
                    await update.message.reply_text(
                        "✅ **Wallet Deleted Successfully!**\n\n"
                        "Your wallet and all associated data have been permanently removed.\n\n"
                        "You can now bind a new wallet using:\n"
                        "/wallet add <private_key>"
                    )
                else:
                    # Cancel deletion
                    context.user_data['pending_wallet_deletion'] = False
                    await update.message.reply_text(
                        "❌ **Wallet Deletion Cancelled**\n\n"
                        "Your wallet remains unchanged.\n\n"
                        "Use /wallet to manage your wallet."
                    )
                return
            
            # Check if message contains token symbols or investment-related keywords
            investment_keywords = ['investment', 'buy', 'sell', 'analysis', 'price', 'trend', 'btc', 'eth', 'coin']
            
            if any(keyword in message_text for keyword in investment_keywords):
                # Provide helpful response
                response = """
💡 **Investment Assistant**

I noticed you mentioned investment-related topics. Here are some useful commands:

📈 **Market Analysis:**
• /daily - View today's top gaining tokens
• /analysis <token> - Get AI analysis report

💰 **Trading Operations:**
• /buy <token> <amount> - Buy tokens
• /sellc <token> <amount> - Sell to USDC
• /swap <token1> <amount> <token2> - Token swap

📊 **Account Management:**
• /wallet - Manage wallet
• /balance - Check balance

For specific help, please use the corresponding commands!
                """
                
                await update.message.reply_text(response)
            else:
                # General response
                await update.message.reply_text(
                    "👋 Hello! I'm the TokenShift bot.\n\n"
                    "Use /help to see all available commands, or use /start to get started!"
                )
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing message: {str(e)}")
    
    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        try:
            error_message = f"""
❌ **Error Occurred**

Sorry, there was a problem processing your request.

**Possible solutions:**
• Check if command format is correct
• Ensure network connection is stable
• Try again later

If the problem persists, please contact technical support.

Error details: {str(context.error)}
            """
            
            if update and update.effective_message:
                await update.effective_message.reply_text(error_message)
            
        except Exception as e:
            print(f"Error in error handler: {e}")
    
    async def handle_unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands"""
        try:
            command = update.message.text.split()[0] if update.message.text else "unknown command"
            
            response = f"""
❓ **Unknown command: {command}**

**Available commands:**
/daily - View today's top gaining tokens
/analysis <token> - AI analysis of token trends
/buy <token> <amount> - Buy tokens
/sellc <token> <amount> - Sell to USDC
/sellt <token> <amount> - Sell to USDT
/swap <token1> <amount> <token2> - Token swap
/wallet - Manage wallet
/balance - Check balance
/portfolio - View portfolio
/help - Get help

Use /help for detailed instructions.
            """
            
            await update.message.reply_text(response)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
