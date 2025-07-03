import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()  # loads variables from .env into environment

#Pull key from env and set headers with the key
API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": os.getenv("RIOT_API_KEY")}



def get_champion_data():
    """
    Fetch champion metadata from Riot's Data Dragon.
    Returns the JSON data for all champions.
    """
    url = 'https://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_champion_list():
    """
    Extract a simplified list of champions with their name, ID, and roles (tags).
    """
    data = get_champion_data()
    if not data:
        return []
    champs = data["data"]
    return [
        {"name": champ["name"], "id": champ["id"], "roles": champ["tags"]}
        for champ in champs.values()
    ]

def get_champion_details(champion_id):
    """
    Fetch full details for a single champion from Data Dragon.
    """
    url = f'https://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion/{champion_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'][champion_id]
    return None

# === Get puuid ===
def get_puuid_by_riot_id(game_name, tag_line, region):
    """
    Get puuid by Riot ID (GameName#TagLine)

    Args:
        game_name: The game name part of Riot ID
        tag_line: The tag line part of Riot ID
        region: Regional routing - 'americas', 'europe', or 'asia'

    Returns:
        puuid string if successful, None if not found
    """
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["puuid"]
    elif response.status_code == 404:
        print(f"Riot ID '{game_name}#{tag_line}' not found.")
    elif response.status_code == 403:
        print("Access denied. Check your API key.")
    elif response.status_code == 429:
        print("Rate limit exceeded. Please wait and try again.")
    else:
        print(f"Error {response.status_code}: {response.text}")

    return None

#=== Retrieve match history IDs ===
def get_match_ids(puuid, region="americas", count=20):
    """
    Fetch recent match IDs for a given puuid.
    Returns a list of match ID strings.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

#=== Retrieve game info ===
def get_match_data(match_id, region="americas"):
    """
    Fetch full match data for a given match ID.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def get_personal_champion_stats(game_name, tag_line, count=20):
    """
    Get personal champion performance stats for NA region only.
    """
    puuid = get_puuid_by_riot_id(game_name, tag_line, region="americas")
    if not puuid:
        return {}

    match_ids = get_match_ids(puuid, region="americas", count=count)
    if not match_ids:
        return {}

    from collections import defaultdict
    stats = defaultdict(lambda: {"games": 0, "wins": 0})

    for match_id in match_ids:
        match = get_match_data(match_id, region="americas")
        if not match:
            continue
        for p in match["info"]["participants"]:
            if p["puuid"] == puuid:
                champ = p["championName"]
                stats[champ]["games"] += 1
                if p["win"]:
                    stats[champ]["wins"] += 1

    return stats


