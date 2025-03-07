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
        """Replicates the fetch request from the presale page to retrieve product data."""

        # Step 1: Fetch the presale page HTML
        response = requests.get(self.presale_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page, status code: {response.status_code}")

        # Step 2: Extract the JSON payload from the script tag
        match = re.search(r'body:\s*\'({.*})\'', response.text)
        if not match:
            raise Exception("Could not extract JSON payload from the page.")

        json_payload = match.group(1).replace("\\'", "'")  # Fix escaping issues
        parsed_payload = json.loads(json_payload)

        # Step 3: Make the same POST request to the API
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        api_response = requests.post(self.api_url, json=parsed_payload, headers=headers)
        if api_response.status_code != 200:
            raise Exception(f"Failed to fetch data from API, status code: {api_response.status_code}")

        # Step 4: Convert API response to `LuxuryForLessAPIResponse`
        return LuxuryForLessAPIResponse(**api_response.json())