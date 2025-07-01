import requests

# TODO: Replace with your actual Riot API key if you use endpoints that require it
API_KEY = 'YOUR_API_KEY'
HEADERS = {'X-Riot-Token': API_KEY}

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
