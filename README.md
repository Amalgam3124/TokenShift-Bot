# TokenShift Bot

A powerful Telegram bot for cryptocurrency trading and portfolio management, built with SideShift.ai API and OpenRouter AI integration.

## 🚀 Features

### 📈 Market Analysis
- **Daily Top Gainers**: View today's highest-gaining tokens supported by SideShift
- **AI Analysis**: Get comprehensive token analysis with technical indicators (RSI, MACD, Bollinger Bands)
- **Real-time Data**: Powered by CoinGecko API for accurate market data

### 💱 Trading Operations
- **Token Swapping**: Exchange tokens using SideShift.ai quotes and execution
- **Multi-chain Support**: Trade across Ethereum, Arbitrum, Polygon, BSC, Avalanche, and Optimism
- **Secure Transactions**: All operations use encrypted wallet management

### 🔑 Wallet Management
- **Easy Binding**: Simple `/wallet <private_key>` command to bind your wallet
- **Multi-network**: Single address works across all supported EVM networks
- **Secure Storage**: Private keys encrypted with Fernet encryption
- **Balance Query**: Real-time balance checking for ETH, USDT, and USDC

### 🤖 AI-Powered Insights
- **Technical Analysis**: RSI, MACD, Bollinger Bands, Support/Resistance levels
- **Trend Analysis**: 1D, 3D, 1W, 1M timeframe analysis
- **Investment Recommendations**: AI-generated buy/sell signals and risk assessment

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot and view welcome message | `/start` |
| `/help` | Show all available commands | `/help` |
| `/daily` | View today's top gaining tokens | `/daily` |
| `/analysis <token>` | Get AI analysis of token trends | `/analysis btc` |
| `/wallet <private_key>` | Bind your wallet | `/wallet 0x1234...` |
| `/wallet` | View wallet status | `/wallet` |
| `/delete` | Delete bound wallet | `/delete` |
| `/balance` | Check ETH/USDT/USDC balances | `/balance` |
| `/swap <token1> <amount> <token2>` | Get swap quote | `/swap eth 0.1 btc` |
| `/checkout` | Execute pending swap | `/checkout` |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token
- SideShift.ai API credentials
- OpenRouter API key
- CoinGecko API key (optional, for enhanced features)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tokenshift-bot.git
   cd tokenshift-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env_example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   SIDESHIFT_SECRET=your_sideshift_secret
   SIDESHIFT_AFFILIATE_ID=your_affiliate_id
   COINGECKO_API_KEY=your_coingecko_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_API_BASE=https://openrouter.ai/api/v1
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | Yes |
| `SIDESHIFT_SECRET` | SideShift.ai API secret | Yes |
| `SIDESHIFT_AFFILIATE_ID` | SideShift.ai affiliate ID | Yes |
| `COINGECKO_API_KEY` | CoinGecko API key | No |
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes |
| `OPENROUTER_API_BASE` | OpenRouter API base URL | Yes |

### Supported Networks

- **Ethereum** (Mainnet)
- **Arbitrum** (One)
- **Polygon** (Matic)
- **BSC** (Binance Smart Chain)
- **Avalanche** (C-Chain)
- **Optimism** (Mainnet)

## 🏗️ Architecture

### Project Structure
```
tokenshift/
├── handlers/                    # Command handlers for Telegram bot
│   ├── basic_handlers.py       # /start, /help commands
│   ├── daily_handler.py        # /daily command - top gaining tokens
│   ├── analysis_handler.py     # /analysis command - AI token analysis
│   ├── trade_handlers.py       # /buy, /sellc, /sellt, /swap, /checkout commands
│   ├── wallet_handler.py       # /wallet, /delete, /balance commands
│   ├── checkout_handlers.py    # /checkout_session command
│   └── message_handlers.py     # Text message and error handlers
├── services/                    # Business logic and external API services
│   ├── sideshift_service.py    # SideShift.ai API integration
│   ├── coingecko_service.py    # CoinGecko API for market data
│   ├── ai_service.py           # OpenRouter AI integration
│   ├── balance_service.py      # Blockchain balance queries
│   ├── technical_analysis.py   # Technical indicators calculation
│   └── wallet_utils.py         # Wallet utilities and address derivation
├── database/                    # Database models and management
│   └── models.py               # SQLite database models with encryption
├── config.py                   # Environment configuration loader
├── main.py                     # Bot entry point and application setup
├── requirements.txt            # Python dependencies
├── env_example                 # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Documentation
└── tokenshift.db               # SQLite database (created at runtime)
```
D
### Key Components

- **Handlers**: Process Telegram commands and messages
- **Services**: Handle external API calls and business logic
- **Database**: Encrypted storage for user data and wallets
- **AI Integration**: OpenRouter for token analysis
- **Blockchain Integration**: Direct RPC calls for balance queries

## 🔒 Security

- **Encrypted Storage**: All private keys encrypted with Fernet
- **Secure APIs**: All external API calls use HTTPS
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: Graceful error handling and user feedback

## 📊 Features in Detail

### AI Analysis
The bot provides comprehensive token analysis including:
- **Technical Indicators**: RSI, MACD, Bollinger Bands
- **Support/Resistance**: Dynamic level calculation
- **Trend Analysis**: Multi-timeframe trend assessment
- **Risk Assessment**: 1-10 scale risk evaluation
- **Trading Signals**: Buy/sell recommendations

### Balance Management
- **Real-time Queries**: Direct blockchain RPC calls
- **Multi-token Support**: ETH, USDT, USDC across all networks
- **Unified Address**: Single address works across all EVM networks
- **Secure Display**: Only shows non-zero balances

### Trading Operations
- **Quote System**: Get real-time swap quotes from SideShift
- **Multi-step Process**: Quote first, then execute with confirmation
- **Cross-chain Support**: Trade between different networks
- **Transaction Tracking**: Full transaction history


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

