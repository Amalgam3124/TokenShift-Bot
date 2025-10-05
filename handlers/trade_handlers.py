"""
Trade command handlers - Trading related commands
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.sideshift_service import SideShiftService
from database.models import DatabaseManager

class TradeHandlers:
    """Handle trading related commands"""
    
    def __init__(self):
        self.sideshift = SideShiftService()
        self.db = DatabaseManager()
    
    async def handle_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /buy command - buy tokens with USDT/USDC"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Usage: /buy <token_symbol> <amount>\n"
                    "Example: /buy btc 0.001"
                )
                return
            
            token_symbol = context.args[0].upper()
            amount = float(context.args[1])
            user_id = update.effective_user.id
            
            # Check if user has wallet
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Get quote from SideShift
            quote = self.sideshift.get_quote(
                deposit_coin='usdt',
                deposit_network='ethereum',
                settle_coin=token_symbol,
                settle_network='ethereum',
                deposit_amount=str(amount)
            )
            
            if not quote:
                await update.message.reply_text("❌ Unable to get buy quote")
                return
            
            # Show quote to user
            message = f"💰 **Buy {token_symbol} Quote**\n\n"
            message += f"Pay: {amount} USDT\n"
            message += f"Get: {quote.get('settleAmount', 'N/A')} {token_symbol}\n"
            message += f"Rate: {quote.get('rate', 'N/A')}\n"
            message += f"Network Fee: {quote.get('networkFee', 'N/A')}\n\n"
            message += "⚠️ This feature requires further blockchain interaction implementation"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("❌ Amount must be a valid number")
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_sellc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sellc command - sell tokens to USDC"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Usage: /sellc <token_symbol> <amount>\n"
                    "Example: /sellc btc 0.001"
                )
                return
            
            token_symbol = context.args[0].upper()
            amount = float(context.args[1])
            user_id = update.effective_user.id
            
            # Check if user has wallet
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Get quote from SideShift
            quote = self.sideshift.get_quote(
                deposit_coin=token_symbol,
                deposit_network='ethereum',
                settle_coin='usdc',
                settle_network='ethereum',
                deposit_amount=str(amount)
            )
            
            if not quote:
                await update.message.reply_text("❌ Unable to get sell quote")
                return
            
            # Show quote to user
            message = f"💱 **Sell {token_symbol} to USDC Quote**\n\n"
            message += f"Sell: {amount} {token_symbol}\n"
            message += f"Get: {quote.get('settleAmount', 'N/A')} USDC\n"
            message += f"Rate: {quote.get('rate', 'N/A')}\n"
            message += f"Network Fee: {quote.get('networkFee', 'N/A')}\n\n"
            message += "⚠️ This feature requires further blockchain interaction implementation"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("❌ Amount must be a valid number")
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_sellt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sellt command - sell tokens to USDT"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Usage: /sellt <token_symbol> <amount>\n"
                    "Example: /sellt btc 0.001"
                )
                return
            
            token_symbol = context.args[0].upper()
            amount = float(context.args[1])
            user_id = update.effective_user.id
            
            # Check if user has wallet
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Get quote from SideShift
            quote = self.sideshift.get_quote(
                deposit_coin=token_symbol,
                deposit_network='ethereum',
                settle_coin='usdt',
                settle_network='ethereum',
                deposit_amount=str(amount)
            )
            
            if not quote:
                await update.message.reply_text("❌ Unable to get sell quote")
                return
            
            # Show quote to user
            message = f"💱 **Sell {token_symbol} to USDT Quote**\n\n"
            message += f"Sell: {amount} {token_symbol}\n"
            message += f"Get: {quote.get('settleAmount', 'N/A')} USDT\n"
            message += f"Rate: {quote.get('rate', 'N/A')}\n"
            message += f"Network Fee: {quote.get('networkFee', 'N/A')}\n\n"
            message += "⚠️ This feature requires further blockchain interaction implementation"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("❌ Amount must be a valid number")
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_swap(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /swap command - get swap quote"""
        try:
            if len(context.args) < 3:
                await update.message.reply_text(
                    "❌ Usage: /swap <token1> <amount> <token2>\n"
                    "Example: /swap eth 0.1 btc"
                )
                return
            
            token1 = context.args[0].upper()
            amount = float(context.args[1])
            token2 = context.args[2].upper()
            user_id = update.effective_user.id
            
            # Check if user has wallet
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Get quote from SideShift
            quote = self.sideshift.get_quote(
                deposit_coin=token1,
                deposit_network='ethereum',  # Default to ethereum
                settle_coin=token2,
                settle_network='ethereum',
                deposit_amount=str(amount)
            )
            
            if not quote:
                await update.message.reply_text("❌ Unable to get swap quote")
                return
            
            # Store quote in context for checkout
            context.user_data['pending_quote'] = quote
            context.user_data['swap_details'] = {
                'from_token': token1,
                'to_token': token2,
                'amount': amount
            }
            
            # Show quote to user
            message = f"💱 **Token Swap Quote**\n\n"
            message += f"From: {amount} {token1}\n"
            message += f"To: {quote.get('settleAmount', 'N/A')} {token2}\n"
            message += f"Rate: {quote.get('rate', 'N/A')}\n"
            message += f"Network Fee: {quote.get('networkFee', 'N/A')}\n"
            message += f"Quote ID: `{quote.get('id', 'N/A')}`\n\n"
            message += "✅ Use /checkout to execute this swap"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("❌ Amount must be a valid number")
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /checkout command - execute pending swap"""
        try:
            user_id = update.effective_user.id
            
            # Check if there's a pending quote
            if 'pending_quote' not in context.user_data:
                await update.message.reply_text(
                    "❌ No pending swap to execute\n"
                    "Please use /swap command to get a quote first"
                )
                return
            
            quote = context.user_data['pending_quote']
            swap_details = context.user_data.get('swap_details', {})
            
            # Get user's wallet address
            wallets = self.db.get_user_wallets(user_id)
            if not wallets:
                await update.message.reply_text(
                    "❌ Please bind wallet first\n"
                    "Use /wallet command to bind your wallet"
                )
                return
            
            # Use first wallet address (in real implementation, let user choose)
            wallet_address = wallets[0]['address']
            
            # Create fixed shift
            shift = self.sideshift.create_fixed_shift(quote['id'], wallet_address)
            
            if not shift:
                await update.message.reply_text("❌ Failed to create swap, please try again")
                return
            
            # Store shift info
            context.user_data['active_shift'] = shift
            
            # Show shift details
            message = f"🔄 **Swap Created**\n\n"
            message += f"Swap ID: `{shift.get('id', 'N/A')}`\n"
            message += f"From: {swap_details.get('amount', 'N/A')} {swap_details.get('from_token', 'N/A')}\n"
            message += f"To: {quote.get('settleAmount', 'N/A')} {swap_details.get('to_token', 'N/A')}\n"
            message += f"Deposit Address: `{shift.get('depositAddress', 'N/A')}`\n"
            message += f"Status: {shift.get('status', 'N/A')}\n\n"
            message += "⚠️ Please send tokens to deposit address to complete swap\n"
            message += "Use /status to check swap status"
            
            # Clear pending quote
            del context.user_data['pending_quote']
            del context.user_data['swap_details']
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
    
    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - check swap status"""
        try:
            user_id = update.effective_user.id
            
            # Check if there's an active shift
            if 'active_shift' not in context.user_data:
                await update.message.reply_text(
                    "❌ No active swap\n"
                    "Please use /swap and /checkout to create a swap first"
                )
                return
            
            shift = context.user_data['active_shift']
            shift_id = shift.get('id')
            
            if not shift_id:
                await update.message.reply_text("❌ Invalid swap ID")
                return
            
            # Get current shift status
            current_status = self.sideshift.get_shift_status(shift_id)
            
            if not current_status:
                await update.message.reply_text("❌ Unable to get swap status")
                return
            
            # Update stored shift info
            context.user_data['active_shift'] = current_status
            
            # Show status
            message = f"📊 **Swap Status**\n\n"
            message += f"Swap ID: `{shift_id}`\n"
            message += f"Status: {current_status.get('status', 'N/A')}\n"
            message += f"Progress: {current_status.get('progress', 'N/A')}\n"
            
            if current_status.get('status') == 'complete':
                message += f"✅ Swap completed!\n"
                message += f"Transaction Hash: `{current_status.get('transactionHash', 'N/A')}`\n"
                # Clear completed shift
                del context.user_data['active_shift']
            elif current_status.get('status') == 'failed':
                message += f"❌ Swap failed\n"
                message += f"Reason: {current_status.get('error', 'N/A')}\n"
                # Clear failed shift
                del context.user_data['active_shift']
            else:
                message += f"⏳ Swap in progress...\n"
                message += f"Use /status to check status again"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing command: {str(e)}")
