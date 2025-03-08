import json
import re
from pathlib import Path

import requests

import config
from api.models.api_response import LuxuryForLessAPIResponse

# Define base directory
BASE_DIR = Path(__file__).resolve().parent


class LuxuryForLessAPI:
    def __init__(self):
        self.presale_url = config.PRESALE_URL  # The main page where the script is embedded
        self.api_url = config.API_URL  # The actual API endpoint


    def fetch_api_response(self) -> LuxuryForLessAPIResponse:
        """Extracts product data directly from the RC_VARS script in the page source."""

        # Step 1: Fetch the presale page HTML
        # Fetching as much we can descending, so we don't need to traverse other pages
        cookies = {
            "rc2c-pop": "96",
            "rc2c-sort": "add_date-DESC"
        }

        response = requests.get(self.presale_url, cookies=cookies)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page, status code: {response.status_code}")

        # Step 2: Extract the JSON data from the RC_VARS script
        match = re.search(r'RC_VARS\s*=\s*({.*?});', response.text, re.DOTALL)
        if not match:
            raise Exception("Could not extract RC_VARS data from the page.")

        json_data = match.group(1)

        # Step 3: Parse the JSON and extract relevant data
        parsed_data = json.loads(json_data)

        # Ensure the expected structure exists
        if "data" not in parsed_data or "search" not in parsed_data["data"]:
            raise Exception("Invalid data structure in RC_VARS.")

        # Step 4: Convert extracted data to LuxuryForLessAPIResponse
        return LuxuryForLessAPIResponse(**parsed_data["data"])