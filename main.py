import argparse
import requests
import json
import os
from datetime import datetime
import pprint


CACHE_FILE = 'cache.json'
SEARCH_CHARACTER_BASE_URL = "https://swapi.dev/api/people/?search="


def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_cache(cache: dict):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)


def search_in_cache(query: str, cache: dict) -> list:
    query = query.lower()
    matches = []

    for cached_name, character_data in cache.items():
        if cached_name == 'search_history':
            continue

        if query in cached_name.lower():
            matches.append(character_data)

    return matches


def search_character(name: str, cache: dict) -> list:
    if 'search_history' not in cache:
        cache['search_history'] = []

    search_record = {
        'query': name,
        'timestamp': datetime.now().isoformat(),
        'results': []
    }

    cache_results = search_in_cache(name, cache)
    if cache_results:
        search_record['results'] = [char['name'] for char in cache_results]
        cache['search_history'].append(search_record)
        save_cache(cache)
        return cache_results

    url = f"{SEARCH_CHARACTER_BASE_URL}{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            characters = []
            for character in data['results']:
                homeworld = get_homeworld(character['homeworld'])
                character['homeworld'] = homeworld
                character["timestamp"] = datetime.now().isoformat()
                cache[character['name']] = character
                characters.append(character)
                search_record['results'].append(character['name'])

            cache['search_history'].append(search_record)
            save_cache(cache)
            return characters

    cache['search_history'].append(search_record)
    save_cache(cache)
    return []


def display_character(character: dict):
    print("-" * 30)
    print(f"Name: {character['name']}")
    print(f"Height: {character['height']}")
    print(f"Mass: {character['mass']}")
    print(f"Birth Year: {character['birth_year']}")


def display_search_history(cache: dict):
    if 'search_history' not in cache or not cache['search_history']:
        print("No search history available.")
        return

    print("\nSearch History:")
    print("-" * 30)
    for entry in cache['search_history']:
        timestamp = datetime.fromisoformat(entry['timestamp'])
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        results = entry['results'] if entry['results'] else ['No matches found']

        print(f"Query: {entry['query']}")
        print(f"Time: {formatted_time}")
        print(f"Results: {', '.join(results)}")
        print("-" * 30)


def get_homeworld(url: str) -> dict | None:
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def display_homeworld(homeworld: dict):
    world_name = homeworld['name']

    orbital_period = _parse_value(homeworld['orbital_period'])
    rotation_period = _parse_value(homeworld['rotation_period'])
    population = _parse_value(homeworld['population'])

    print("Homeworld")
    print("-" * 30)
    print(f"Name: {world_name}")
    print(f"Population: {population if population is not None else 'Unknown'}")

    if orbital_period is not None and rotation_period is not None:
        years_on_earth = round(orbital_period / 365, 2)
        days_on_earth = round((rotation_period / 24), 2)
        print(f"On {world_name}, 1 years on earth is {years_on_earth} and 1 day on earth is {days_on_earth}")
    else:
        print(f"On {world_name}, the orbital period and the rotation period are unknown")


def _parse_value(value: str) -> int | None:
    try:
        return int(value)
    except (ValueError, KeyError):
        return None



def main():
    parser = argparse.ArgumentParser(description='Star Wars CLI')
    subparsers = parser.add_subparsers(dest='command')

    search_parser = subparsers.add_parser('search', help='Search for Star Wars characters')
    search_parser.add_argument('name', nargs='+', type=str, help="Name of the character to search for")
    search_parser.add_argument("--world", action="store_true", help="Include homeworld information")

    cache_parser = subparsers.add_parser('cache', help='Cache operations')
    cache_parser.add_argument('operation', choices=['clean', 'history'], help="Cache file")
    args = parser.parse_args()

    if args.command == 'search':
        search_query = ' '.join(args.name)
        cache = load_cache()
        characters = search_character(search_query, cache)
        if characters:
            print(f"Found {len(characters)} matches:")
            for character in characters:
                display_character(character)
                if args.world:
                    print("\n")
                    display_homeworld(character['homeworld'])
                print("\n")
                if character['timestamp']:
                    print(f"Cached: {character['timestamp']}")
        else:
            print("The Force is not strong enough within you")
    elif args.command == 'cache':
        cache = load_cache()
        if args.operation == 'clean':
            os.remove(CACHE_FILE)
            print('Removed cache')
        elif args.operation == 'history':
            display_search_history(cache)


if __name__ == '__main__':
    main()

