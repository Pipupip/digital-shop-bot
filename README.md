# Digital Shop Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram" alt="Aiogram">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

A Telegram bot for selling digital goods — activation keys, PDF guides, subscriptions, and promo codes. Fully automated delivery after payment.

## Features

- Product catalog with categories
- Product cards with descriptions and prices
- Shopping cart and order management
- Instant auto-delivery after payment simulation
- Purchase history database
- Inline keyboards for smooth navigation

## Tech Stack

- **Python** 3.10+
- **Aiogram** 3.x
- **SQLite**
- **Inline Keyboards**

## Installation

```bash
git clone https://github.com/pipupip/digital-shop-bot
cd digital-shop-bot
pip install -r requirements.txt
```

## Configuration

Edit `config.py` and provide your bot token:

```python
BOT_TOKEN = "your-telegram-bot-token"
```

## Running

```bash
python bot.py
```

## Project Structure

```
bot_2_digital_shop/
├── bot.py              # Entry point
├── config.py           # Configuration
├── database.py         # Database layer
├── requirements.txt    # Dependencies
└── handlers/           # Bot message handlers
```

## Deployment

Deploy on any VPS or cloud platform (Railway, Render, etc.). Set `BOT_TOKEN` as an environment variable in your deployment environment.

---

<p align="center">Built with ❤️ by <a href="https://github.com/pipupip">pipupip</a></p>
