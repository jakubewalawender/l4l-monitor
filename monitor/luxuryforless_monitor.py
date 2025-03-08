import asyncio
import os
import re
import requests
import config
from dotenv import load_dotenv
from api.luxuryforless_api import LuxuryForLessAPI
from api.models.api_response import LuxuryForLessAPIResponse
from db import SQLiteDatabase
from logging_config import setup_logging  # Import the logging setup

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


class LuxuryForLessMonitor:
    UNWANTED_KEYWORDS = [
        "dezodorant", "deodorant", "świeca", "świeczka"
    ]

    def __init__(self) -> None:
        # Set up logging
        self.info_logger, self.exception_logger = setup_logging()  # Use the logging setup from logging_config.py

        self.CHECK_INTERVAL = config.CHECK_INTERVAL  # Get from config.py
        self.NOTIFICATIONS_ENABLED = config.NOTIFICATIONS_ENABLED  # Get from config.py
        self.luxury = LuxuryForLessAPI()
        self.db = SQLiteDatabase()  # Create instance of SQLiteDatabase

    async def check_for_updates(self) -> None:
        self.info_logger.info("Starting LuxuryForLess Monitor...")
        while True:
            try:
                # Fetch the latest response from the API
                response = self.luxury.fetch_api_response()

                # Retrieve stored product IDs from the database
                stored_ids = self.db.retrieve_product_ids()

                # If there are no stored product IDs, skip notifications
                if not stored_ids:
                    self.info_logger.info("No stored product IDs, skipping notifications.")
                else:
                    # Otherwise, get new products based on the comparison of stored IDs
                    new_products = self.get_new_products(stored_ids, response)
                    if new_products:
                        self.info_logger.info(f"New products detected: {len(new_products)}")
                        if self.NOTIFICATIONS_ENABLED:
                            self.notify_user(new_products)
                    else:
                        self.info_logger.info("No new products detected.")

                # Store the new product IDs to the database (this will replace the old IDs)
                product_ids = [product.products_id for search in response.search for product in search.products]
                self.db.store_product_ids(product_ids)  # Save the new product IDs to the database

            except Exception as e:
                self.exception_logger.error(f"Error fetching data: {e}", exc_info=True)  # Log exception with traceback

            await asyncio.sleep(self.CHECK_INTERVAL)

    def get_new_products(self, stored_ids: list, new_data: LuxuryForLessAPIResponse):
        """Compares stored product IDs with the new ones after filtering unwanted products."""

        # Extract only the products that are not in the stored list AND not unwanted
        new_products = [
            product for search in new_data.search for product in search.products
            if product.products_id not in stored_ids and not any(keyword.lower() in product.name.lower() for keyword in self.UNWANTED_KEYWORDS)
        ]

        return new_products


    def escape_markdown_v2(self, text: str) -> str:
        """Escapes special characters for Telegram MarkdownV2."""
        special_chars = r'_*[\]()~`>#+-=|{}.!'
        return re.sub(r'([%s])' % re.escape(special_chars), r'\\\1', text)

    def notify_user(self, new_products):
        """Sends new product notifications to Telegram."""
        for product in new_products:
            message = f"🛑️ *Znak ubytkowy* 🛑\n\n" \
                      f"🧴 *{self.escape_markdown_v2(product.name)}*\n" \
                      f"💰 Cena: {self.escape_markdown_v2(product.promotions_price_brutto)} {self.escape_markdown_v2(product.currency)}\n" \
                      f"🔗 [Link]({self.escape_markdown_v2(product.url)})"

            self.send_telegram_message(message, product.main_image)

    def send_telegram_message(self, text: str, image_url: str):
        """Sends a message with an image to the Telegram channel."""
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": config.TELEGRAM_CHANNEL_ID,
            "photo": image_url,
            "caption": text,
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": True
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.info_logger.info("Notification sent to Telegram.")
            else:
                self.exception_logger.error(f"Failed to send message: {response.text}")
        except Exception as e:
            self.exception_logger.error(f"Error sending Telegram message: {e}", exc_info=True)
