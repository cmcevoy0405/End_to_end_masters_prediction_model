import pandas as pd
import requests



X_API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"
url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4"
}

def fetch_player_top10s(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "138",   # Replace "120" with the relevant stat ID if needed
        "year": year,      # Replace 2022 with the relevant year
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

    if response.status_code == 200:
        data = response.json()

        # Extract the player stats
        rows = data.get('data', {}).get('statDetails', {}).get('rows', [])

        player_stats = []
        for row in rows:
            if row.get('__typename') == 'StatDetailsPlayer':
                player_name = row.get('playerName')
                top_10s = 0
                firsts = 0
                for stat in row.get('stats', []):
                    stat_name = stat.get('statName')
                    stat_value = stat.get('statValue', '0')  # Get the stat value, default to '0'

                    # Only convert to int if the stat_value is a digit
                    if stat_value.isdigit():
                        stat_value = int(stat_value)
                    else:
                        stat_value = 0  # Handle non-numeric values (like '-') as 0

                    if stat_name == "Top 10":
                        top_10s = stat_value
                    elif stat_name == "1st":
                        firsts = stat_value
                player_stats.append({
                    'player_name': player_name,
                    'Top 10 Finishes': top_10s,
                    '1st_place_finishes': firsts,
                    'year': year
                })

        return pd.DataFrame(player_stats)

all_stats = []
for year in range(2005, 2025+1):
    stats_data = fetch_player_top10s(year)
    all_stats.append(stats_data)

# Combine all the stats into a single DataFrame
final_df = pd.concat(all_stats, ignore_index=True)
final_df=final_df.drop(columns=['Top 10 Finishes'])

final_df.to_csv('wins.csv', index=False)
