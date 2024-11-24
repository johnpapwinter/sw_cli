from datetime import datetime
from typing import Optional, Dict, List

import requests

from cache import Cache


class StarWarsCLI:
    BASE_URL = "https://swapi.dev/api/people/?search="

    def __init__(self, cache_file: str):
        self.cache = Cache(cache_file)

    def get_homeworld(self, url: str) -> Optional[Dict]:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def search_api(self, name: str) -> List[Dict]:
        response = requests.get(f"{self.BASE_URL}{name}")
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                characters = []
                for character in data['results']:
                    character['homeworld'] = self.get_homeworld(character['homeworld'])
                    character['timestamp'] = datetime.now().isoformat()
                    characters.append(character)
                return characters
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
