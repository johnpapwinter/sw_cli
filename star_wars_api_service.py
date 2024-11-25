import json
from datetime import datetime
from typing import Optional, Dict, List

import requests

from cache import Cache


class StarWarsAPIService:
    BASE_URL = "https://swapi.dev/api/people/?search="

    def __init__(self, cache_file: str):
        self.cache = Cache(cache_file)

    def get_homeworld(self, url: str) -> Optional[Dict]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: Could not fetch homeworld data. {str(e)}")
            return None
        except json.JSONDecodeError:
            print("Error: Received invalid homeworld data from the Star Wars API")
            return None

    def search_api(self, name: str) -> List[Dict]:
        try:
            response = requests.get(f"{self.BASE_URL}{name}")
            response.raise_for_status()  # Raises an exception for 4XX/5XX status codes
            data = response.json()
            if data['results']:
                characters = []
                for character in data['results']:
                    try:
                        character['homeworld'] = self.get_homeworld(character['homeworld'])
                        character['timestamp'] = datetime.now().isoformat()
                        characters.append(character)
                    except requests.RequestException:
                        print(f"Warning: Could not fetch homeworld data for {character['name']}")
                return characters
            return []
        except requests.RequestException as e:
            print(f"Error: Could not complete the search request. {str(e)}")
            return []
        except json.JSONDecodeError:
            print("Error: Received invalid data from the Star Wars API")
            return []

    def search(self, query: str) -> List[Dict]:
        # Try cache first
        characters = self.cache.search_characters(query)

        if characters:
            self.cache.add_search_record(query, [char['name'] for char in characters])
            return characters

        # If not in cache, search API
        characters = self.search_api(query)
        if characters:
            # Cache the results
            for character in characters:
                self.cache.data[character['name']] = character

            self.cache.add_search_record(query, [char['name'] for char in characters])
            self.cache.save()

        return characters

    @staticmethod
    def display_character(character: Dict):
        print("-" * 30)
        print(f"Name: {character['name']}")
        print(f"Height: {character['height']}")
        print(f"Mass: {character['mass']}")
        print(f"Birth Year: {character['birth_year']}")
        if 'timestamp' in character:
            print(f"\nCached: {character['timestamp']}")

    @staticmethod
    def display_homeworld(homeworld: Dict):
        print("Homeworld")
        print("-" * 30)
        print(f"Name: {homeworld['name']}")

        try:
            population = int(homeworld['population'])
            print(f"Population: {population}")
        except (ValueError, KeyError):
            print("Population: Unknown")

        try:
            orbital_period = int(homeworld['orbital_period'])
            rotation_period = int(homeworld['rotation_period'])
            years_on_earth = round(orbital_period / 365, 2)
            days_on_earth = round(rotation_period / 24, 2)
            print(f"On {homeworld['name']}, 1 year on earth is {years_on_earth} and 1 day on earth is {days_on_earth}")
        except (ValueError, KeyError):
            print(f"On {homeworld['name']}, the orbital period and the rotation period are unknown")
