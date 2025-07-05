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
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4"}

def fetch_masters_results(year):
    year = f"{year}0"
    payload = {
            "operationName": "TournamentPastResults",
            "variables": {
                "tournamentPastResultsId": "R2023014",
                "year": year
            },
            "query": """
                query TournamentPastResults($tournamentPastResultsId: ID!, $year: Int) {
                tournamentPastResults(id: $tournamentPastResultsId, year: $year) {
                    id
                    players {
                    id
                    position
                    player {
                        id
                        firstName
                        lastName
                        shortName
                        displayName
                        abbreviations
                        abbreviationsAccessibilityText
                        amateur
                        country
                        countryFlag
                        lineColor
                        seed
                        status
                        tourBound
                        assets {
                        ... on TourBoundAsset {
                            tourBoundLogo
                            tourBoundLogoDark
                        }
                        }
                    }
                    rounds {
                        score
                        parRelativeScore
                    }
                    additionalData
                    total
                    parRelativeScore
                    }
                    teams {
                    teamId
                    position
                    players {
                        id
                        firstName
                        lastName
                        shortName
                        displayName
                        abbreviations
                        abbreviationsAccessibilityText
                        amateur
                        country
                        countryFlag
                        lineColor
                        seed
                        status
                        tourBound
                        assets {
                        ... on TourBoundAsset {
                            tourBoundLogo
                            tourBoundLogoDark
                        }
                        }
                    }
                    additionalData
                    total
                    parRelativeScore
                    rounds {
                        score
                        parRelativeScore
                    }
                    }
                    rounds
                    additionalDataHeaders
                    availableSeasons {
                    year
                    displaySeason
                    }
                    winner {
                    id
                    firstName
                    lastName
                    totalStrokes
                    totalScore
                    countryFlag
                    countryName
                    purse
                    displayPoints
                    displayPurse
                    points
                    seed
                    pointsLabel
                    winnerIcon {
                        type
                        title
                        label
                        color
                    }
                    }
                    winningTeam {
                    id
                    firstName
                    lastName
                    totalStrokes
                    totalScore
                    countryFlag
                    countryName
                    purse
                    displayPoints
                    displayPurse
                    points
                    seed
                    pointsLabel
                    winnerIcon {
                        type
                        title
                        label
                        color
                    }
                    }
                    recap {
                    weather {
                        day
                        text
                    }
                    notes
                    }
                }
                }
            """
        }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        players = data.get('data', {}).get('tournamentPastResults', {}).get('players', [])

        player_postion = []

        for player_info in players:
            position = player_info.get('position')
            display_name = player_info.get('player', {}).get('displayName', 'Unknown Player')

            stats_dict = {
                'player_id' : player_info['id'],
                'player_name' : display_name,
                'position' : position,
                'year' : year
            }
            player_postion.append(stats_dict)

        return player_postion
    
def save_to_s3(data, year):
    if not data:
        print(f"No data to upload for {year}")
        return
    
    file_key = f"raw/results/masters_results_{year}.ndjson"
    njson_data = "\n".join(json.dumps(record, ensure_ascii=False) for record in data)

    s3_client.put_object(Bucket = S3_BUCKET, Key = file_key, Body = njson_data)
    print(f"Uploaded data: {file_key} for {year}")


start_year = datetime.now().year - 20
end_year = datetime.now().year

all_years_data = []

for year in range(start_year, end_year + 1):
    masters_data = fetch_masters_results(year)
    if masters_data:
        all_years_data.extend(masters_data)
        print(f"Fetched data for {year}")
    else:
        print(f"No data for {year}")

if all_years_data:
    df = pd.DataFrame(all_years_data)
    df['year'] = df['year'].astype(str).str.rstrip("0")
    df.to_csv("masters_results.csv", index=False)
    print("Saved all masters results")

print("Data extraction complete")


        
