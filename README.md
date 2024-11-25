# Star Wars CLI

A command-line interface tool for searching Star Wars characters using the [SWAPI](https://swapi.dev/) (Star Wars API). The tool includes caching functionality to improve performance and track search history.

## Features

- Search for Star Wars characters by name (case-insensitive, partial matches supported)
- View detailed character information including:
  - Name
  - Height
  - Mass
  - Birth Year
- Optional homeworld information display including:
  - Planet name
  - Population
  - Orbital and rotation periods (compared to Earth)
- Caching system that:
  - Stores previous search results
  - Maintains search history
  - Improves response time for repeated searches

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd star-wars-cli
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Search for Characters

Basic search:
```bash
python main.py search luke
```

Search with homeworld information:
```bash
python main.py search "anakin skywalker" --world
```

### Cache Operations

View search history:
```bash
python main.py cache history
```

Clean cache:
```bash
python main.py cache clean
```

### Command Reference

```bash
# General help
python main.py --help

# Search command help
python main.py search --help

# Cache command help
python main.py cache --help
```

## Output Examples

### Character Search
```
Found 1 matches:
------------------------------
Name: Luke Skywalker
Height: 172
Mass: 77
Birth Year: 19BBY

Cached: 2024-11-25T10:30:15.123456
```

### Character Search with Homeworld
```
Found 1 matches:
------------------------------
Name: Luke Skywalker
Height: 172
Mass: 77
Birth Year: 19BBY

Homeworld
------------------------------
Name: Tatooine
Population: 200000
On Tatooine, 1 year on earth is 1.02 and 1 day on earth is 0.96

Cached: 2024-11-25T10:30:15.123456
```

### Search History
```
Search History:
------------------------------
Query: luke
Time: 2024-11-25 10:30:15
Results: Luke Skywalker
------------------------------
```

## Project Structure

```
star-wars-cli/
├── main.py                    # CLI entry point
├── star_wars_api_service.py   # Main service class
├── cache.py                   # Cache handling
├── requirements.txt           # Project dependencies
└── README.md                 # Documentation
```

## Dependencies

- `requests`: For making HTTP requests to SWAPI
- `argparse`: For parsing command line arguments

