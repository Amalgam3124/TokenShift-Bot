"""
Checkout command handlers - Checkout related commands
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.sideshift_service import SideShiftService
from database.models import DatabaseManager

class CheckoutHandlers:
    """Handle checkout related commands"""
    
    def __init__(self):
        self.sideshift = SideShiftService()
        self.db = DatabaseManager()
    
    async def handle_checkout_session(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /checkout_session command - create checkout session for easy purchase"""
        try:
            if len(context.args) < 3:
                await update.message.reply_text(
                    "❌ Usage: /checkout_session <token> <amount> <network>\n"
                    "Example: /checkout_session eth 0.01 mainnet"
                )
                return
            
            token = context.args[0].upper()
            amount = context.args[1]
            network = context.args[2].lower()
            user_id = update.effective_user.id
            
            # Check if user has wallet
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Use first wallet address
            wallet_address = wallets[0]['address']
            
            # Create checkout session
            checkout = self.sideshift.create_checkout_session(
                settle_coin=token,
                settle_network=network,
                settle_amount=amount,
                settle_address=wallet_address,
                success_url="https://t.me/your_bot?start=success",
                cancel_url="https://t.me/your_bot?start=cancel"
            )
            
            if not checkout:
                await update.message.reply_text("❌ Failed to create checkout session")
                return
            
            # Show checkout details
            message = f"🛒 **Checkout Session Created**\n\n"
            message += f"Token: {amount} {token}\n"
            message += f"Network: {network}\n"
            message += f"Address: `{wallet_address}`\n"
            message += f"Session ID: `{checkout.get('id', 'N/A')}`\n\n"
            
            if 'url' in checkout:
                message += f"🔗 Checkout Link: {checkout['url']}\n\n"
            
            message += "✅ Checkout session created successfully!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
