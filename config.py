import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# General Config
CHECK_INTERVAL = 120  # X seconds (adjust as needed)
NOTIFICATIONS_ENABLED = True  # Set up notifications later (e.g., Firebase, Telegram)

# URLs and API endpoints
BASE_URL = os.getenv("BASE_URL")
PRESALE_URL = os.getenv("PRESALE_URL")
API_URL = os.getenv("API_URL")

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Database Path (SQLite)
DB_PATH = os.getenv("DB_PATH", "luxury_for_less.db")  # Default to "luxury_for_less.db" if not set in .env
