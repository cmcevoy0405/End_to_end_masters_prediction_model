import requests
import pandas as pd

import requests

# Define the endpoint URL and headers
url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4"  # Replace with your actual API key
}

# Define the payload with the correct variable names
payload = """
{
tournamentPastResults(id: "R2023014", year: 20240) {
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

# Make the POST request
response = requests.post(url, json={'query': payload}, headers=headers)

# Check for a successful response
if response.status_code == 200:
    data = response.json()

    # Extract player information
    players = data.get('data', {}).get('tournamentPastResults', {}).get('players', [])

    player_data = []
    for player_info in players:
        display_name = player_info.get('player', {}).get('displayName', 'Unknown Player')

        player_data.append({
            'Player Name': display_name
        })

    # Convert to DataFrame
    df_players = pd.DataFrame(player_data)
    print(df_players)
else:
    raise Exception(f"Request failed with status code {response.status_code}: {response.text}")


print(df_players)

X_API_KEY = "da2-gsrx5bibzbb4njvhl7t37wqyl4"

def fetch_player_score(year):
    payload = {
        "operationName": "StatDetails",
        "variables": {
            "tourCode": "R",
            "statId": "120",
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
    if response.status_code == 200:
        data = response.json()


        rows = data['data']['statDetails'].get('rows', [])
        player_avg_stats = {}
        for row in rows:
            # Check if '__typename' is present and correctly identifies 'StatDetailsPlayer'
            if 'playerName' in row:
                player_name = row['playerName']
                avg_stat_value = next((stat['statValue'] for stat in row.get('stats', []) if stat['statName'] == 'Avg'), None)
                if avg_stat_value is not None:
                    player_avg_stats[player_name] = avg_stat_value
        return pd.DataFrame(player_avg_stats.items(), columns=['Player Name', 'Avg_score']).assign(Year=year)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player data for past 5 years
df_score_avg_2024 = fetch_player_score(2024)
df_score_avg_2023 = fetch_player_score(2023)
df_score_avg_2022 = fetch_player_score(2022)
df_score_avg_2021 = fetch_player_score(2021)
df_score_avg_2020 = fetch_player_score(2020)
df_score_avg_2019 = fetch_player_score(2019)
df_score_avg_2018 = fetch_player_score(2018)
df_score_avg_2017 = fetch_player_score(2017)
df_score_avg_2016 = fetch_player_score(2016)
df_score_avg_2015 = fetch_player_score(2015)
df_score_avg_2014 = fetch_player_score(2014)
df_score_avg_2013 = fetch_player_score(2013)
df_score_avg_2012 = fetch_player_score(2012)
df_score_avg_2011 = fetch_player_score(2011)
df_score_avg_2010 = fetch_player_score(2010)
df_score_avg_2009 = fetch_player_score(2009)
df_score_avg_2008 = fetch_player_score(2008)

# Combine data for both years
df_player_score = pd.concat([df_score_avg_2024, df_score_avg_2023, df_score_avg_2022, df_score_avg_2021, df_score_avg_2020, df_score_avg_2019, df_score_avg_2018, df_score_avg_2017, df_score_avg_2016, df_score_avg_2015, df_score_avg_2014, df_score_avg_2013,
                                df_score_avg_2012, df_score_avg_2011, df_score_avg_2010, df_score_avg_2009, df_score_avg_2008], ignore_index=True)

print(df_player_score)


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
                    'Player Name': player_name,
                    'Top 10 Finishes': top_10s,
                    '1st Place Finishes': firsts,
                    'Year': year
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = fetch_player_top10s(2024)
df_stats_2023 = fetch_player_top10s(2023)
df_stats_2022 = fetch_player_top10s(2022)
df_stats_2021 = fetch_player_top10s(2021)
df_stats_2020 = fetch_player_top10s(2020)
df_stats_2019 = fetch_player_top10s(2019)
df_stats_2018 = fetch_player_top10s(2018)
df_stats_2017 = fetch_player_top10s(2017)
df_stats_2016 = fetch_player_top10s(2016)
df_stats_2015 = fetch_player_top10s(2015)
df_stats_2014 = fetch_player_top10s(2014)
df_stats_2013 = fetch_player_top10s(2013)
df_stats_2012 = fetch_player_top10s(2012)
df_stats_2011 = fetch_player_top10s(2011)
df_stats_2010 = fetch_player_top10s(2010)
df_stats_2009 = fetch_player_top10s(2009)
df_stats_2008 = fetch_player_top10s(2008)

# Combine data for all years
df_player_finishes = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015,df_stats_2014, df_stats_2013,
                                    df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_player_finishes)}")
print(df_player_finishes)

def fetch_drive_distance(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "101",   # Replace "120" with the relevant stat ID if needed
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
                drive_avg = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == "Avg":  # Adjust based on actual stat name
                        drive_avg = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year': year,
                    'Drive Avg': drive_avg  # Rename "Avg" to "Drive Avg"
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = fetch_drive_distance(2024)
df_stats_2023 = fetch_drive_distance(2023)
df_stats_2022 = fetch_drive_distance(2022)
df_stats_2021 = fetch_drive_distance(2021)
df_stats_2020 = fetch_drive_distance(2020)
df_stats_2019 = fetch_drive_distance(2019)
df_stats_2018 = fetch_drive_distance(2018)
df_stats_2017 = fetch_drive_distance(2017)
df_stats_2016 = fetch_drive_distance(2016)
df_stats_2015 = fetch_drive_distance(2015)
df_stats_2014 = fetch_drive_distance(2014)
df_stats_2013 = fetch_drive_distance(2013)
df_stats_2012 = fetch_drive_distance(2012)
df_stats_2011 = fetch_drive_distance(2011)
df_stats_2010 = fetch_drive_distance(2010)
df_stats_2009 = fetch_drive_distance(2009)
df_stats_2008 = fetch_drive_distance(2008)


# Combine data for all years
df_drivedis_stats = pd.concat([df_stats_2024,df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                                df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_drivedis_stats)}")
print(df_drivedis_stats)

def fetch_drive_accuracy(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "102",   # Replace "120" with the relevant stat ID if needed
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
                percent_fairways_hit = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == "%":  # Adjust based on actual stat name
                        percent_fairways_hit = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year': year,
                    '%_of_fairways_hit': percent_fairways_hit  # Rename "% Fairways Hit" to "%_of_fairways_hit"
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = fetch_drive_accuracy(2024)
df_stats_2023 = fetch_drive_accuracy(2023)
df_stats_2022 = fetch_drive_accuracy(2022)
df_stats_2021 = fetch_drive_accuracy(2021)
df_stats_2020 = fetch_drive_accuracy(2020)
df_stats_2019 = fetch_drive_accuracy(2019)
df_stats_2018 = fetch_drive_accuracy(2018)
df_stats_2017 = fetch_drive_accuracy(2017)
df_stats_2016 = fetch_drive_accuracy(2016)
df_stats_2015 = fetch_drive_accuracy(2015)
df_stats_2014 = fetch_drive_accuracy(2014)
df_stats_2013 = fetch_drive_accuracy(2013)
df_stats_2012 = fetch_drive_accuracy(2012)
df_stats_2011 = fetch_drive_accuracy(2011)
df_stats_2010 = fetch_drive_accuracy(2010)
df_stats_2009 = fetch_drive_accuracy(2009)
df_stats_2008 = fetch_drive_accuracy(2008)

# Combine data for all years
df_driveacc = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_driveacc)}")
print(df_driveacc)

def fetch_putts_per_round(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "119",   # Replace "120" with the relevant stat ID if needed
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
                putts_per_round = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        putts_per_round = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year' : year,
                    'Putts per round': putts_per_round
                })


        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

df_stats_2024 = fetch_putts_per_round(2024)
df_stats_2023 = fetch_putts_per_round(2023)
df_stats_2022 = fetch_putts_per_round(2022)
df_stats_2021 = fetch_putts_per_round(2021)
df_stats_2020 = fetch_putts_per_round(2020)
df_stats_2019 = fetch_putts_per_round(2019)
df_stats_2018 = fetch_putts_per_round(2018)
df_stats_2017 = fetch_putts_per_round(2017)
df_stats_2016 = fetch_putts_per_round(2016)
df_stats_2015 = fetch_putts_per_round(2015)
df_stats_2014 = fetch_putts_per_round(2014)
df_stats_2013 = fetch_putts_per_round(2013)
df_stats_2012 = fetch_putts_per_round(2012)
df_stats_2011 = fetch_putts_per_round(2011)
df_stats_2010 = fetch_putts_per_round(2010)
df_stats_2009 = fetch_putts_per_round(2009)
df_stats_2008 = fetch_putts_per_round(2008)

# Combine data for all years
df_putts = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                        df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_putts)}")
print(df_putts)

def fetch_scramble(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "130",   # Replace "120" with the relevant stat ID if needed
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
                scramble_percentage = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == '%':
                        scramble_percentage = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year' : year,
                    'Scramble %' : scramble_percentage
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

df_stats_2024 = fetch_scramble(2024)
df_stats_2023 = fetch_scramble(2023)
df_stats_2022 = fetch_scramble(2022)
df_stats_2021 = fetch_scramble(2021)
df_stats_2020 = fetch_scramble(2020)
df_stats_2019 = fetch_scramble(2019)
df_stats_2018 = fetch_scramble(2018)
df_stats_2017 = fetch_scramble(2017)
df_stats_2016 = fetch_scramble(2016)
df_stats_2015 = fetch_scramble(2015)
df_stats_2014 = fetch_scramble(2014)
df_stats_2013 = fetch_scramble(2013)
df_stats_2012 = fetch_scramble(2012)
df_stats_2011 = fetch_scramble(2011)
df_stats_2010 = fetch_scramble(2010)
df_stats_2009 = fetch_scramble(2009)
df_stats_2008 = fetch_scramble(2008)

# Combine data for all years
df_scramble = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_scramble)}")
print(df_scramble)

def fetch_gir(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "103",   # Replace "120" with the relevant stat ID if needed
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
                gir = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == '%':
                        gir = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'GIR %' : gir
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

df_stats_2024 = fetch_gir(2024)
df_stats_2023 = fetch_gir(2023)
df_stats_2022 = fetch_gir(2022)
df_stats_2021 = fetch_gir(2021)
df_stats_2020 = fetch_gir(2020)
df_stats_2019 = fetch_gir(2019)
df_stats_2018 = fetch_gir(2018)
df_stats_2017 = fetch_gir(2017)
df_stats_2016 = fetch_gir(2016)
df_stats_2015 = fetch_gir(2015)
df_stats_2014 = fetch_gir(2014)
df_stats_2013 = fetch_gir(2013)
df_stats_2012 = fetch_gir(2012)
df_stats_2011 = fetch_gir(2011)
df_stats_2010 = fetch_gir(2010)
df_stats_2009 = fetch_gir(2009)
df_stats_2008 = fetch_gir(2008)

# Combine data for all years
df_gir = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                        df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_gir)}")
print(df_gir)

def fetch_bounce_back(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "160",   # Replace "120" with the relevant stat ID if needed
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
                bounce_back = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == '%':
                        bounce_back = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year': year,
                    'Bounce_Back %': bounce_back
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

df_stats_2024 = fetch_bounce_back(2024)
df_stats_2023 = fetch_bounce_back(2023)
df_stats_2022 = fetch_bounce_back(2022)
df_stats_2021 = fetch_bounce_back(2021)
df_stats_2020 = fetch_bounce_back(2020)
df_stats_2019 = fetch_bounce_back(2019)
df_stats_2018 = fetch_bounce_back(2018)
df_stats_2017 = fetch_bounce_back(2017)
df_stats_2016 = fetch_bounce_back(2016)
df_stats_2015 = fetch_bounce_back(2015)
df_stats_2014 = fetch_bounce_back(2014)
df_stats_2013 = fetch_bounce_back(2013)
df_stats_2012 = fetch_bounce_back(2012)
df_stats_2011 = fetch_bounce_back(2011)
df_stats_2010 = fetch_bounce_back(2010)
df_stats_2009 = fetch_bounce_back(2009)
df_stats_2008 = fetch_bounce_back(2008)


df_bounce_back = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                                df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

print(f"Total Rows in Stats DataFrame: {len(df_bounce_back)}")
print(df_bounce_back)

def sg_total(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02675",   # Replace "120" with the relevant stat ID if needed
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
                total_sg = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        total_sg = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'Total Strokes Gained' : total_sg
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_total(2024)
df_stats_2023 = sg_total(2023)
df_stats_2022 = sg_total(2022)
df_stats_2021 = sg_total(2021)
df_stats_2020 = sg_total(2020)
df_stats_2019 = sg_total(2019)
df_stats_2018 = sg_total(2018)
df_stats_2017 = sg_total(2017)
df_stats_2016 = sg_total(2016)
df_stats_2015 = sg_total(2015)
df_stats_2014 = sg_total(2014)
df_stats_2013 = sg_total(2013)
df_stats_2012 = sg_total(2012)
df_stats_2011 = sg_total(2011)
df_stats_2010 = sg_total(2010)
df_stats_2009 = sg_total(2009)
df_stats_2008 = sg_total(2008)

# Combine data for all years
df_total_sg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_total_sg)}")
print(df_total_sg)

def sg_off_tee(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02567",   # Replace "120" with the relevant stat ID if needed
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
                sg_off_tee = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        sg_off_the_tee = stat.get('statValue', '0')

                    # Convert stat_value to int if it's a digit, otherwise keep as string
                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'SG:OTT' : sg_off_the_tee
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_off_tee(2024)
df_stats_2023 = sg_off_tee(2023)
df_stats_2022 = sg_off_tee(2022)
df_stats_2021 = sg_off_tee(2021)
df_stats_2020 = sg_off_tee(2020)
df_stats_2019 = sg_off_tee(2019)
df_stats_2018 = sg_off_tee(2018)
df_stats_2017 = sg_off_tee(2017)
df_stats_2016 = sg_off_tee(2016)
df_stats_2015 = sg_off_tee(2015)
df_stats_2014 = sg_off_tee(2014)
df_stats_2013 = sg_off_tee(2013)
df_stats_2012 = sg_off_tee(2012)
df_stats_2011 = sg_off_tee(2011)
df_stats_2010 = sg_off_tee(2010)
df_stats_2009 = sg_off_tee(2009)
df_stats_2008 = sg_off_tee(2008)


# Combine data for all years
df_sg_ott = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                        df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_sg_ott)}")
print(df_sg_ott)

def sg_round_green(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02569",   # Replace "120" with the relevant stat ID if needed
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
                sg_arg = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        sg_arg = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year' : year,
                    'SG:ARG' : sg_arg
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_round_green(2024)
df_stats_2023 = sg_round_green(2023)
df_stats_2022 = sg_round_green(2022)
df_stats_2021 = sg_round_green(2021)
df_stats_2020 = sg_round_green(2020)
df_stats_2019 = sg_round_green(2019)
df_stats_2018 = sg_round_green(2018)
df_stats_2017 = sg_round_green(2017)
df_stats_2016 = sg_round_green(2016)
df_stats_2015 = sg_round_green(2015)
df_stats_2014 = sg_round_green(2014)
df_stats_2013 = sg_round_green(2013)
df_stats_2012 = sg_round_green(2012)
df_stats_2011 = sg_round_green(2011)
df_stats_2010 = sg_round_green(2010)
df_stats_2009 = sg_round_green(2009)
df_stats_2008 = sg_round_green(2008)

# Combine data for all years
df_sg_round_green = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                                df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_sg_round_green)}")
print(df_sg_round_green)

def sg_ttg(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02674",   # Replace "120" with the relevant stat ID if needed
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
                sg_ttg = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        sg_ttg = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'SG:TTG' : sg_ttg
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_ttg(2024)
df_stats_2023 = sg_ttg(2023)
df_stats_2022 = sg_ttg(2022)
df_stats_2021 = sg_ttg(2021)
df_stats_2020 = sg_ttg(2020)
df_stats_2019 = sg_ttg(2019)
df_stats_2018 = sg_ttg(2018)
df_stats_2017 = sg_ttg(2017)
df_stats_2016 = sg_ttg(2016)
df_stats_2015 = sg_ttg(2015)
df_stats_2014 = sg_ttg(2014)
df_stats_2013 = sg_ttg(2013)
df_stats_2012 = sg_ttg(2012)
df_stats_2011 = sg_ttg(2011)
df_stats_2010 = sg_ttg(2010)
df_stats_2009 = sg_ttg(2009)
df_stats_2008 = sg_ttg(2008)

# Combine data for all years
df_ttg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                        df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_ttg)}")
print(df_ttg)

def sg_apg(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02568",   # Replace "120" with the relevant stat ID if needed
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
                sg_apg = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        sg_apg = stat.get('statValue', '0')

                    # Convert stat_value to int if it's a digit, otherwise keep as string
                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'SG:APG' : sg_apg
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_apg(2024)
df_stats_2023 = sg_apg(2023)
df_stats_2022 = sg_apg(2022)
df_stats_2021 = sg_apg(2021)
df_stats_2020 = sg_apg(2020)
df_stats_2019 = sg_apg(2019)
df_stats_2018 = sg_apg(2018)
df_stats_2017 = sg_apg(2017)
df_stats_2016 = sg_apg(2016)
df_stats_2015 = sg_apg(2015)
df_stats_2014 = sg_apg(2014)
df_stats_2013 = sg_apg(2013)
df_stats_2012 = sg_apg(2012)
df_stats_2011 = sg_apg(2011)
df_stats_2010 = sg_apg(2010)
df_stats_2009 = sg_apg(2009)
df_stats_2008 = sg_apg(2008)

# Combine data for all years
df_sg_apg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                        df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_sg_apg)}")
print(df_sg_apg)

def sg_putting(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "02564",   # Replace "120" with the relevant stat ID if needed
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
                sg_putting = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        sg_putting = stat.get('statValue', '0')

                    # Convert stat_value to int if it's a digit, otherwise keep as string
                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'SG:PUTT' : sg_putting
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = sg_putting(2024)
df_stats_2023 = sg_putting(2023)
df_stats_2022 = sg_putting(2022)
df_stats_2021 = sg_putting(2021)
df_stats_2020 = sg_putting(2020)
df_stats_2019 = sg_putting(2019)
df_stats_2018 = sg_putting(2018)
df_stats_2017 = sg_putting(2017)
df_stats_2016 = sg_putting(2016)
df_stats_2015 = sg_putting(2015)
df_stats_2014 = sg_putting(2014)
df_stats_2013 = sg_putting(2013)
df_stats_2012 = sg_putting(2012)
df_stats_2011 = sg_putting(2011)
df_stats_2010 = sg_putting(2010)
df_stats_2009 = sg_putting(2009)
df_stats_2008 = sg_putting(2008)

# Combine data for all years
df_sg_putting = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_sg_putting)}")
print(df_sg_putting)

def par_3_avg(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "142",   # Replace "120" with the relevant stat ID if needed
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
                par_3_score = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        par_3_score = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name': player_name,
                    'Year' : year,
                    'Par 3 Score' : par_3_score
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = par_3_avg(2024)
df_stats_2023 = par_3_avg(2023)
df_stats_2022 = par_3_avg(2022)
df_stats_2021 = par_3_avg(2021)
df_stats_2020 = par_3_avg(2020)
df_stats_2019 = par_3_avg(2019)
df_stats_2018 = par_3_avg(2018)
df_stats_2017 = par_3_avg(2017)
df_stats_2016 = par_3_avg(2016)
df_stats_2015 = par_3_avg(2015)
df_stats_2014 = par_3_avg(2014)
df_stats_2013 = par_3_avg(2013)
df_stats_2012 = par_3_avg(2012)
df_stats_2011 = par_3_avg(2011)
df_stats_2010 = par_3_avg(2010)
df_stats_2009 = par_3_avg(2009)
df_stats_2008 = par_3_avg(2008)

# Combine data for all years
df_par_3_avg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_par_3_avg)}")
print(df_par_3_avg)

def par_4_avg(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "143",   # Replace "120" with the relevant stat ID if needed
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
                par_4_score = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        par_4_score = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'Par 4 score' : par_4_score
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = par_4_avg(2024)
df_stats_2023 = par_4_avg(2023)
df_stats_2022 = par_4_avg(2022)
df_stats_2021 = par_4_avg(2021)
df_stats_2020 = par_4_avg(2020)
df_stats_2019 = par_4_avg(2019)
df_stats_2018 = par_4_avg(2018)
df_stats_2017 = par_4_avg(2017)
df_stats_2016 = par_4_avg(2016)
df_stats_2015 = par_4_avg(2015)
df_stats_2014 = par_4_avg(2014)
df_stats_2013 = par_4_avg(2013)
df_stats_2012 = par_4_avg(2012)
df_stats_2011 = par_4_avg(2011)
df_stats_2010 = par_4_avg(2010)
df_stats_2009 = par_4_avg(2009)
df_stats_2008 = par_4_avg(2008)

# Combine data for all years
df_par_4_avg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_par_4_avg)}")
print(df_par_4_avg)

def par_5_avg(year):
    payload = {
    "operationName": "StatDetails",
    "variables": {
        "tourCode": "R",  # Replace "R" with the relevant tour code if needed
        "statId": "144",   # Replace "120" with the relevant stat ID if needed
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
                par_5_score = None

                for stat in row.get('stats', []):
                    if stat.get('statName') == 'Avg':
                        par_5_score = stat.get('statValue', '0')

                player_stats.append({
                    'Player Name' : player_name,
                    'Year' : year,
                    'Par 5 score' : par_5_score
                })

        return pd.DataFrame(player_stats)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player stats for the years 2023 through 2019
df_stats_2024 = par_5_avg(2024)
df_stats_2023 = par_5_avg(2023)
df_stats_2022 = par_5_avg(2022)
df_stats_2021 = par_5_avg(2021)
df_stats_2020 = par_5_avg(2020)
df_stats_2019 = par_5_avg(2019)
df_stats_2018 = par_5_avg(2018)
df_stats_2017 = par_5_avg(2017)
df_stats_2016 = par_5_avg(2016)
df_stats_2015 = par_5_avg(2015)
df_stats_2014 = par_5_avg(2014)
df_stats_2013 = par_5_avg(2013)
df_stats_2012 = par_5_avg(2012)
df_stats_2011 = par_5_avg(2011)
df_stats_2010 = par_5_avg(2010)
df_stats_2009 = par_5_avg(2009)
df_stats_2008 = par_5_avg(2008)

# Combine data for all years
df_par_5_avg = pd.concat([df_stats_2024, df_stats_2023, df_stats_2022, df_stats_2021, df_stats_2020, df_stats_2019, df_stats_2018, df_stats_2017, df_stats_2016, df_stats_2015, df_stats_2014, df_stats_2013,
                            df_stats_2012, df_stats_2011, df_stats_2010, df_stats_2009, df_stats_2008], ignore_index=True)

# Display the final DataFrame
print(f"Total Rows in Stats DataFrame: {len(df_par_5_avg)}")
print(df_par_5_avg)

def fetch_masters_results(year):
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

        player_data = []
        for player_info in players:
            position = player_info.get('position')
            display_name = player_info.get('player', {}).get('displayName', 'Unknown Player')

            player_data.append({
                'Player Name' : display_name,
                'Year': year,
                'Masters Finish' : position
            })

        return pd.DataFrame(player_data)
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Fetch player data for the years 2023 through 2019
years = [20230, 20220, 20210, 20200, 20190, 20180, 20170, 20160, 20150, 20140, 20130, 20120, 20110, 20100, 20090, 20080]
df_list = []

for year in years:
    df_year = fetch_masters_results(year)
    df_list.append(df_year)

# Combine data for all years
df_masters_finish = pd.concat(df_list, ignore_index=True)

df_masters_finish['Year'] = df_masters_finish['Year'].astype(str).str.rstrip('0')
# Convert the 'Year' column back to integer if needed
df_masters_finish['Year'] = df_masters_finish['Year'].astype(int)

# Display the final DataFrame
print(f"Total Rows in Player Data DataFrame: {len(df_masters_finish)}")
print(df_masters_finish)


#FINAL DF DATA ---------------------------------------------------------------------------------------------------------------------------------


df_stats = [df_player_score, df_player_finishes, df_drivedis_stats, df_driveacc, df_putts, df_gir, df_scramble, df_bounce_back, df_total_sg, df_sg_ott
            , df_sg_round_green, df_ttg, df_sg_apg, df_sg_putting, df_par_3_avg, df_par_4_avg, df_par_5_avg, df_masters_finish]

df_final = df_stats[0]

for stat in df_stats[1:]:
    if not stat.empty:
        df_final = pd.merge(df_final, stat, on = ['Player Name', 'Year'], how = 'outer')

df_masters_stats = df_final[df_final['Player Name'].isin(df_players['Player Name'])]

df_masters_stats.set_index('Player Name', inplace = True)

# Display the filtered DataFrame
print(f"Total Rows in Filtered DataFrame: {len(df_masters_stats)}")
print(df_masters_stats)

df_masters_stats.to_csv('masters_data.csv')



