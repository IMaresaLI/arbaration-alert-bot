# 🧠 Crypto Arbitrage Alert Bot

A Python-based cryptocurrency arbitrage bot that compares prices across multiple exchanges to detect and log arbitrage opportunities in real-time.

---

## 📌 Features

- ✅ Real-time price comparison across multiple exchanges  
- 🔄 Multi-threaded price fetching for speed  
- ⚙️ Configurable through `config.ini`  
- 💾 Saves all data (arbitrage, prices, successes)  
- 📡 Telegram and Discord integration  
- 🖥️ User-friendly CLI menu interface  

---

## 🚀 How It Works

The bot fetches live price data from supported exchanges and compares them using user-defined thresholds. When a potential arbitrage is found, it logs the data, sends optional notifications, and stores it for analysis.

---

## 🧪 Menu Options

Upon running, you'll see a CLI menu:

| Option | Description |
|--------|-------------|
| 1 | Start Arbitrage Check |
| 2 | Check Status / Stop Bot |
| 3 | View Arbitrage Data (Opportunities, Success Logs, Price Logs) |
| 4 | Config Overview |
| 5 | Exit the Program |

---

## ⚙️ Configuration (`config.ini`)

```ini
[Exchange Details]
Binance = https://api.binance.com/api/v3/ticker/price?symbol=SYMBOL
Binance_Status = 1
Mexc = https://api.mexc.com/api/v3/ticker/price?symbol=SYMBOL
Mexc_Status = 1
KuCoin = https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=SYMBOL
KuCoin_Status = 1
Coinbase = https://api.exchange.coinbase.com/products/SYMBOL/ticker
Coinbase_Status = 1
OKX = https://www.okx.com/api/v5/market/ticker?instId=SYMBOL
OKX_Status = 1
Gate.io = https://api.gateio.ws/api/v4/spot/tickers?currency_pair=SYMBOL
Gate.io_Status = 1
BingX = https://open-api.bingx.com/openApi/swap/v2/quote/bookTicker?symbol=SYMBOL
BingX_Status = 1
Bitget = https://api.bitget.com/api/v2/spot/market/tickers?symbol=SYMBOL
Bitget_Status = 1

[Arbitrage Settings]
SYMBOLS = DOGE-USDT,ETH-USDT,BTC-USDT
ARBITRAGE_THRESHOLD = 1.0, 0.5, 1.5
TIMER_INTERVAL = 5
PRICES_SAVE = 1
ARBITRAGE_SAVE = 1
ARBITRAGE_SUCCESS_SAVE = 1
MULTI_PROCESSING = 1

[Database]
MAIN_FOLDER = database
ARBITRAGE_JSON = arbitrage.json
ARBITRAGE_SUCCESS = arbitrage_success.json
PRICES = prices.json

[Telegram]
TELEGRAM_BOT_TOKEN = <your_token>
TELEGRAM_CHAT_ID = <your_chat_id>
NOTIFICATION_STATUS = 0

[Discord]
DISCORD_WEBHOOK = <your_webhook_url>
NOTIFICATION_STATUS = 0
```

---

## 🌐 Supported Exchanges

- Binance  
- Mexc  
- KuCoin  
- Coinbase  
- OKX  
- Gate.io  
- BingX  
- Bitget  

> Enable or disable any exchange in the `[Exchange Details]` section of `config.ini`.

---

## 📦 Requirements

- **Python** 3.7 or higher  
- **Dependencies:**
  - `requests`
  - `configparser`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 📁 Folder Structure

```bash
├── config/
│   ├── __init__.py
│   └── config.ini
├── database/
│   ├── arbitrage.json
│   ├── arbitrage_success.json
│   └── prices.json
├── core/
│   ├── __init__.py
│   ├── arbitrage_handler.py
│   ├── data_handler.py
│   ├── data_handler_SQL.py [DISABLED]
│   ├── noti_handler.py
│   └── exchange_handler.py
├── logs/
│   └── arbitrage.log            
├── requirements.txt
└── main.py
```

---

## 🧠 Planned Features

- 🗃️ Data conversion to different formats
- 🔧 Automatic trading support for selected exchanges
- 📊 Web dashboard with real-time arbitrage charts
- 📈 Dynamic threshold and symbol management
- 💰 Built-in profit calculator 

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Feel free to fork this project, submit PRs, or suggest features via GitHub Issues!

---

## 🙏 Support This Project

If this bot helps you save time or profit from arbitrage, consider showing some ❤️ to support its further development:

### 💖 Donate

- **USDT (TRC20)**: `TVwZC8TPqEXDRJWyUrnT6BnFU628MTZHci`
- **BTC**: `1PAstxtBMTi8UhrfsYCpqEMQWU9q1FjT9J`  
- **Ethereum (ERC20)**: `0x3ab33035fd184b409de454d6eece985ab0823beb`  

### 🧡 Become a Sponsor

Get early access to premium features and sponsor-only tools.  
📬 Contact via GitHub or email below for sponsor tiers.

---

## 📬 Contact

- GitHub Issues – for bugs and feedback  
- Email – `bytearchsoft@gmail.com` (for business inquiries or sponsorships)