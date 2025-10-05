"""
Wallet command handler - Wallet management
"""
from telegram import Update
from telegram.ext import ContextTypes
from database.models import DatabaseManager
from services.wallet_utils import WalletUtils
from services.balance_service import BalanceService

class WalletHandler:
    """Handle wallet related commands"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.wallet_utils = WalletUtils()
        self.balance_service = BalanceService()
    
    async def handle_wallet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /wallet command - manage wallet"""
        try:
            if not context.args:
                # Show current wallets
                user_id = update.effective_user.id
                wallets = self.db.get_user_wallets(user_id)
                
                if not wallets:
                    await update.message.reply_text(
                        "🔑 **Wallet Management**\n\n"
                        "You haven't bound a wallet yet\n\n"
                        "Bind wallet: /wallet <private_key>\n"
                        "Delete wallet: /delete\n\n"
                        "Supports all EVM networks: Ethereum, Arbitrum, Polygon, BSC, Avalanche, Optimism"
                    )
                else:
                    message = "🔑 **Wallet Status**\n\n"
                    message += "✅ Wallet is bound and ready\n\n"
                    message += "💡 Commands:\n"
                    message += "• /wallet <private_key> - Bind new wallet\n"
                    message += "• /delete - Delete current wallet\n"
                    message += "• /balance - Check balance"
                    
                    await update.message.reply_text(message, parse_mode='Markdown')
                
                return
            
            # Direct private key binding
            private_key = context.args[0]
            user_id = update.effective_user.id
            
            # Check if user already has wallets
            if self.db.has_wallets(user_id):
                await update.message.reply_text(
                    "⚠️ You already have a wallet bound!\n\n"
                    "Please delete your current wallet first:\n"
                    "/delete\n\n"
                    "Then you can bind a new wallet."
                )
                return
            
            # Validate private key
            if not self.wallet_utils.is_valid_private_key(private_key):
                await update.message.reply_text(
                    "❌ Invalid private key format\n"
                    "Please provide a valid 64-character hexadecimal private key"
                )
                return
            
            # Convert private key to address
            address = self.wallet_utils.private_key_to_address(private_key)
            
            if not address:
                await update.message.reply_text(
                    "❌ Failed to derive address from private key\n"
                    "Please check your private key and try again"
                )
                return
            
            # Add wallet to database for all EVM networks
            evm_networks = self.wallet_utils.get_evm_networks()
            for network in evm_networks:
                self.db.add_wallet(user_id, network["name"].lower(), address, private_key)
            
            await update.message.reply_text(
                f"✅ Wallet added successfully!\n"
                f"Address: `{address}`\n"
                f"Supported on all EVM networks: Ethereum, Arbitrum, Polygon, BSC, Avalanche, Optimism",
                parse_mode='Markdown'
            )
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /delete command - delete wallet with confirmation"""
        try:
            user_id = update.effective_user.id
            
            # Check if user has wallets
            if not self.db.has_wallets(user_id):
                await update.message.reply_text(
                    "❌ You don't have any wallet bound!\n\n"
                    "Use /wallet add <private_key> to bind a wallet first."
                )
                return
            
            # Store confirmation state
            context.user_data['pending_wallet_deletion'] = True
            
            await update.message.reply_text(
                "⚠️ **Confirm Wallet Deletion**\n\n"
                "This will permanently delete your bound wallet and all associated data.\n\n"
                "Type `confirm` to proceed with deletion, or send any other message to cancel.\n\n"
                "**This action cannot be undone!**"
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")

    async def handle_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command - check USDT/USDC balance"""
        try:
            user_id = update.effective_user.id
            wallets = self.db.get_user_wallets(user_id)
            
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Get the first wallet address (all networks use same address)
            wallet_address = wallets[0]['address']
            
            # Send loading message
            loading_msg = await update.message.reply_text("🔍 Querying balances across networks...")
            
            # Get balances from all networks
            balances = self.balance_service.get_wallet_balances(wallet_address)
            
            # Format and send balance message
            message = self.balance_service.format_balance_message(balances)
            
            await loading_msg.edit_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
