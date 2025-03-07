import asyncio
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Response

import config
from api.models.api_response import LuxuryForLessAPIResponse

# Define base directory
BASE_DIR = Path(__file__).resolve().parent


class LuxuryForLessAPI:
    def __init__(self):
        # Define URLs and API endpoints
        self.base_url = config.BASE_URL
        self.presale_url = config.PRESALE_URL
        self.api_url = config.API_URL

    async def fetch_api_response(self) -> LuxuryForLessAPIResponse:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Headless mode for Raspberry Pi
            page = await browser.new_page()

            response_data: Optional[LuxuryForLessAPIResponse] = None

            # Function to capture API response
            async def intercept(response: Response) -> None:
                nonlocal response_data
                if self.api_url in response.url:
                    json_data = await response.json()
                    response_data = LuxuryForLessAPIResponse(**json_data)

            page.on("response", intercept)

            await page.goto(self.presale_url)
            await asyncio.sleep(5)  # Wait for JavaScript execution
            await browser.close()

            if response_data is None:
                raise ValueError("Failed to fetch data from API.")

            return response_data

