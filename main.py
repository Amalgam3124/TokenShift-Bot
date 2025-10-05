"""
TokenShift Telegram Bot - Main Application
"""
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.basic_handlers import BasicHandlers
from handlers.daily_handler import DailyHandler
from handlers.analysis_handler import AnalysisHandler
from handlers.trade_handlers import TradeHandlers
from handlers.checkout_handlers import CheckoutHandlers
from handlers.wallet_handler import WalletHandler
from handlers.message_handlers import MessageHandlers
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TokenShiftBot:
    """Main bot class"""
    
    def __init__(self):
        self.config = Config()
        self.basic_handlers = BasicHandlers()
        self.daily_handler = DailyHandler()
        self.analysis_handler = AnalysisHandler()
        self.trade_handlers = TradeHandlers()
        self.checkout_handlers = CheckoutHandlers()
        self.wallet_handler = WalletHandler()
        self.message_handlers = MessageHandlers()
        
        # Validate configuration
        if not self.config.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        if not self.config.SIDESHIFT_SECRET:
            raise ValueError("SIDESHIFT_SECRET is required")
        if not self.config.SIDESHIFT_AFFILIATE_ID:
            raise ValueError("SIDESHIFT_AFFILIATE_ID is required")
    
    def create_application(self) -> Application:
        """Create and configure the bot application"""
        
        # Create application
        application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.basic_handlers.handle_start))
        application.add_handler(CommandHandler("help", self.basic_handlers.handle_help))
        application.add_handler(CommandHandler("daily", self.daily_handler.handle_daily))
        application.add_handler(CommandHandler("analysis", self.analysis_handler.handle_analysis))
        application.add_handler(CommandHandler("buy", self.trade_handlers.handle_buy))
        application.add_handler(CommandHandler("sellc", self.trade_handlers.handle_sellc))
        application.add_handler(CommandHandler("sellt", self.trade_handlers.handle_sellt))
        application.add_handler(CommandHandler("swap", self.trade_handlers.handle_swap))
        application.add_handler(CommandHandler("checkout", self.trade_handlers.handle_checkout))
        application.add_handler(CommandHandler("status", self.trade_handlers.handle_status))
        application.add_handler(CommandHandler("checkout_session", self.checkout_handlers.handle_checkout_session))
        application.add_handler(CommandHandler("wallet", self.wallet_handler.handle_wallet))
        application.add_handler(CommandHandler("delete", self.wallet_handler.handle_delete))
        application.add_handler(CommandHandler("balance", self.wallet_handler.handle_balance))
        
        # Add message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                             self.message_handlers.handle_text_message))
        
        # Add error handler
        application.add_error_handler(self.message_handlers.handle_error)
        
        return application
    
    def start_bot(self):
        """Start the bot"""
        try:
            logger.info("Starting TokenShift Bot...")
            
            # Create application
            application = self.create_application()
            
            # Start polling
            logger.info("Bot started polling...")
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
    
    async def stop_bot(self):
        """Stop the bot"""
        logger.info("Stopping TokenShift Bot...")
        # Cleanup code here if needed

def main():
    """Main function"""
    try:
        # Create bot instance
        bot = TokenShiftBot()
        
        # Start the bot
        bot.start_bot()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
