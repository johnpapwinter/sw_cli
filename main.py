import argparse

from star_wars_api_service import StarWarsAPIService


def main():
    parser = argparse.ArgumentParser(description='Star Wars CLI')
    subparsers = parser.add_subparsers(dest='command')

    search_parser = subparsers.add_parser('search', help='Search for Star Wars characters')
    search_parser.add_argument('name', nargs='+', type=str, help="Name of the character to search for")
    search_parser.add_argument("--world", action="store_true", help="Include homeworld information")

    cache_parser = subparsers.add_parser('cache', help='Cache operations')
    cache_parser.add_argument('operation', choices=['clean', 'history'], help="Cache operations: clean or show history")

    args = parser.parse_args()
    cli = StarWarsAPIService('cache.json')

    if args.command == 'search':
        search_query = ' '.join(args.name)
        characters = cli.search(search_query)

        if characters:
            print(f"Found {len(characters)} matches:")
            for character in characters:
                cli.display_character(character)
                if args.world and character.get('homeworld'):
                    print("\n")
                    cli.display_homeworld(character['homeworld'])
                print()
        else:
            print("The Force is not strong enough within you")

    elif args.command == 'cache':
        if args.operation == 'clean':
            cli.cache.clean()
            print('Removed cache')
        elif args.operation == 'history':
            cli.cache.display_search_history()


if __name__ == '__main__':
    main()


