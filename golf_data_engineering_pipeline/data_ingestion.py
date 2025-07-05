import datetime
import json
import requests
import pandas as pd


url = 'https://www.masters.com/en_US/cms/feeds/players/2025/invitees.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'application/json',  # Adjust as needed
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_players():
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("API error, could not fetch data")

    data = response.json()
    invitees = data['invitees']

    masters_players = []

    for player in invitees:
        stats_dict = {
            'player_name': f"{player['firstname']} {player['lastname']}",
            'country': player['country']
        }
        masters_players.append(stats_dict)
    return masters_players

def save_to_csv(data):
    if not data:
        print("No data to save")
        return

    df = pd.DataFrame(data)
    file_name = f"masters_players_{datetime.datetime.now().year}.csv"
    df.to_csv(file_name, index=False)
    print(f"Saved locally as {file_name}")

# Fetch & Save
masters_players = fetch_players()
save_to_csv(masters_players)




