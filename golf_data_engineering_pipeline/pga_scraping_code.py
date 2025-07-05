import requests
import pandas as pd
from datetime import datetime
import json
import boto3

S3_BUCKET = 'pgagolfstats'
s3_client = boto3.client('s3')

X_API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"
url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4"
}

stats_to_fetch = {
    "120": "avg_score",
    "138": "top_10",
    "101": "drive_dist",
    "102": "drive_acc",
    "119": "putts_per_round",
    "130": "scramble",
    "103": "gir",
    "160": "bounce_back",
    "02675": "strokes_gained",
    "02567": "strokes_gained_ot",
    "02569": "strokes_gained_arg",
    "02674": "strokes_gained_ttg",
    "02568": "strokes_gained_atg",
    "02564": "strokes_gained_putt",
    "142": "par3_score",
    "143": "par4_score",
    "144": "par5_score"
}

def fetch_player_stat(stat_id, year):
    payload = {
        "operationName": "StatDetails",
        "variables": {
            "tourCode": "R",
            "statId": stat_id,
            "year": year,
            "eventQuery": None
        },
        "query": """
            query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {
            statDetails(
                tourCode: $tourCode
                statId: $statId
                year: $year
                eventQuery: $eventQuery
        ) {
                __typename
                tourCode
                year
                displaySeason
                statId
                statType
                tournamentPills {
                tournamentId
                displayName
                }
                yearPills {
                year
                displaySeason
                }
                statTitle
                statDescription
                tourAvg
                lastProcessed
                statHeaders
                statCategories {
                category
                displayName
                subCategories {
                    displayName
                    stats {
                    statId
                    statTitle
                    }
                }
                }
                rows {
                ... on StatDetailsPlayer {
                    __typename
                    playerId
                    playerName
                    country
                    countryFlag
                    rank
                    rankDiff
                    rankChangeTendency
                    stats {
                    statName
                    statValue
                    color
                    }
                }
                ... on StatDetailTourAvg {
                    __typename
                    displayName
                    value
                }
                }
                sponsorLogo
            }
            }
        """
        }               
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Api error for {stat_id} ({year}): {response.status_code}")
        return []
    
    data = response.json()
    rows = data.get('data', {}).get('statDetails', {}).get('rows', [])
    player_stats = []
        
    for row in rows:
            # Check if 'playerName' is in the row
        if 'playerName' in row:
            stat_value_keys = ['Avg', '%', 'Top 10', '1st']
            stat_value = next((s['statValue'] for s in row['stats'] if s['statName'] in stat_value_keys), None)
            
            # Ensure rank is an integer
            rank = int(row['rank']) if row.get('rank') is not None else None

            stats_dict = {
                'player_id' : row['playerId'],
                'player_name': row['playerName'],
                'year': year,
                'rank': rank,
                'stat_id': stat_id,
                'stat_name': stats_to_fetch.get(stat_id, f"stat_{stat_id}"),
                'stat_value': stat_value
            }
            player_stats.append(stats_dict)
        
    print(f"Fetched {len(player_stats)} players for {stat_id} ({year})")
    return player_stats


start_year = datetime.now().year - 20
end_year = datetime.now().year

all_stats = []

for year in range(start_year, end_year + 1):
    for stat_id in stats_to_fetch.keys():
        stats_data = fetch_player_stat(stat_id, year)
        all_stats.extend(stats_data)
    
df = pd.DataFrame(all_stats)
df['stat_value'] = df['stat_value'].replace({'%': ''}, regex=True)  # Remove the '%' sign
df['stat_value'] = pd.to_numeric(df['stat_value'], errors='coerce')

df = df.pivot_table(
    index=['player_id', 'player_name', 'year'],
    columns='stat_name',
    values='stat_value'
).reset_index()


print(df.head())
print(df.isna().sum())

df.to_csv('player_stats.csv', index=False)

        
print("Data extraction completed!")



