import json
import os
from datetime import datetime
from typing import List, Dict


class Cache:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.data, file)

    def clean(self):
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            self.data = {}

    def search_characters(self, query: str) -> List[Dict]:
        query = query.lower()
        matches = []

        for cached_name, character_data in self.data.items():
            if cached_name == 'search_history':
                continue
            if query in cached_name.lower():
                matches.append(character_data)

        return matches

    def add_search_record(self, query: str, results: List[str]):
        if 'search_history' not in self.data:
            self.data['search_history'] = []

        self.data['search_history'].append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results': results
        })
        self.save()

    def display_search_history(self):
        if 'search_history' not in self.data or not self.data['search_history']:
            print("No search history available.")
            return

        print("\nSearch History:")
        print("-" * 30)
        for entry in self.data['search_history']:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            results = entry['results'] if entry['results'] else ['No matches found']

            print(f"Query: {entry['query']}")
            print(f"Time: {formatted_time}")
            print(f"Results: {', '.join(results)}")
            print("-" * 30)
