import json

import requests
from django.core.management.base import BaseCommand, CommandError


class APIException(CommandError):
    """Exception for API connection errors"""

    pass


def validate_data(data):
    if not isinstance(data, list):
        raise ValueError("Received data is not a list.")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Invalid data type: expected a list of dictionaries.")
        if not all(key in item for key in ["id", "name", "is_active", "tags"]):
            raise ValueError("Missing required keys in dictionary.")
        if not isinstance(item["id"], int):
            raise ValueError("Field 'id' is not an integer.")
        if not isinstance(item["name"], str):
            raise ValueError("Field 'name' is not a string.")
        if not isinstance(item["is_active"], bool):
            raise ValueError("Field 'is_active' is not a boolean.")
        if not isinstance(item["tags"], list) or not all(
            isinstance(tag, str) for tag in item["tags"]
        ):
            raise ValueError("Field 'tags' is not a list of strings.")


class Command(BaseCommand):
    help = "Downloads data from an external API and displays it."

    def handle(self, *args, **options):
        url = "https://nonexistent.example.com/api/data"  # False URL

        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise APIException(
                    f"HTTP error: Expected 200 OK, got {response.status_code}"
                )

            try:
                data = response.json()
                validate_data(data)

                self.stdout.write(self.style.SUCCESS("API data downloaded and parsed:"))
                for item in data:
                    self.stdout.write(f"  ID: {item['id']}")
                    self.stdout.write(f"  Name: {item['name']}")
                    self.stdout.write(f"  Is Active: {item['is_active']}")
                    self.stdout.write(f"  Tags: {item['tags']}")
                    self.stdout.write("")

            except json.JSONDecodeError:
                raise ValueError("API response is not valid JSON.")
            except ValueError as e:
                raise ValueError(f"Invalid data type from API: {e}")

        except requests.exceptions.ConnectionError as e:
            raise APIException(f"API connection error: {e}")
