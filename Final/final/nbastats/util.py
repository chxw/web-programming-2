import requests
import datetime
import re
import random

nba_endpoint = "https://data.nba.net/data/10s/prod/v1/"
headshot_endpoint = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/1040x760/"
logo_endpoint = "https://cdn.nba.com/logos/nba/"


def random_players():
    year = datetime.date.today().year
    url = nba_endpoint+str(year)+"/players.json"

    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]

    found_players = []
    for player in players:
        if player["nbaDebutYear"]:
            found_players.append(player)

    return random.sample(found_players, 5)


def search_players(query):
    year = datetime.date.today().year
    url = nba_endpoint+str(year)+"/players.json"

    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]

    found_players = []
    for player in players:
        full_name = ' '.join([player["firstName"], player["lastName"]])
        if re.search(query, full_name, re.IGNORECASE) and player["nbaDebutYear"]:
            found_players.append(player)

    return found_players


def get_season_avgs(player_id):
    year = datetime.date.today().year
    url = nba_endpoint+str(year)+"/players/"+str(player_id)+"_profile.json"

    response = requests.request("GET", url)
    response_json = response.json()
    reg_season = response_json['league']['standard']['stats']['regularSeason']['season']

    season_averages = []
    for season in reg_season:
        datapt = season['total']
        datapt['season'] = season['seasonYear']
        season_averages.append(datapt)

    return season_averages


def get_player_info(player_id):
    year = datetime.date.today().year
    url = nba_endpoint+str(year)+"/players.json"

    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]
    player = [player for player in players if player["personId"]
              == str(player_id)]

    try:
        return player[0]
    except IndexError:
        return None


def get_player_photo(player_id):
    url = headshot_endpoint+str(player_id)+".png"
    return url


def get_team_name(team_id):
    year = datetime.date.today().year
    url = nba_endpoint+str(year)+"/teams.json"

    response = requests.request("GET", url)
    data = response.json()
    teams = data["league"]["standard"]
    team = [team for team in teams if team["teamId"] == str(team_id)]

    try:
        return team[0]["fullName"]
    except IndexError:
        return None


def get_team_photo(team_id):
    url = logo_endpoint+str(team_id)+"/primary/D/logo.svg"
    return url
