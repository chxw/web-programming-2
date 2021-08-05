import requests
import datetime
import re

from json.decoder import JSONDecodeError
from urllib.parse import quote
from django.core.paginator import Paginator

# HELPER FUNCTIONS
def get_page(request, results):
    page_number = request.GET.get('page', 1) # 1 is default
    paginator = Paginator(results, 10)
    page = paginator.page(page_number)
    return page

# BALLDONTLIE.IO functions

teams_endpoint = "https://www.balldontlie.io/api/v1/teams/"
players_endpoint = "https://www.balldontlie.io/api/v1/players/"
stats_endpoint = "https://www.balldontlie.io/api/v1/stats/"
season_endpoint = "https://www.balldontlie.io/api/v1/season_averages/"

def get_team_name(id):
    url = teams_endpoint+str(id)

    response = requests.request("GET", url)
    data = response.json()
    return data["full_name"]

def get_players(query):
    results = []
    page = 1

    while True:
        url = players_endpoint+"?"+"page="+str(page)+"&"+"search="+quote(str(query))
        response = requests.request("GET", url)
        try:
            data = response.json()
            results.append(data["data"])
        except (JSONDecodeError, IndexError):
            break
        page += 1

    return [page for sublist in results for page in sublist]

def search_players(query):
    print(query)
    results = []

    year = datetime.date.today().year
    url = "https://data.nba.net/data/10s/prod/v1/"+str(year)+"/players.json"

    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]

    found_players = []
    for player in players:
        full_name = ' '.join([player["firstName"], player["lastName"]])
        if re.search(query, full_name, re.IGNORECASE):
            found_players.append(player)

    return found_players


def get_season_avgs(player_id):
    url = "https://data.nba.net/data/10s/prod/v1/2020/players/"+str(player_id)+"_profile.json"

    response = requests.request("GET", url)
    response_json = response.json()
    reg_season = response_json['league']['standard']['stats']['regularSeason']['season']


    season_averages = []
    for season in reg_season: 
        datapt = season['total']
        datapt['season'] = season['seasonYear']
        season_averages.append(datapt)

    return season_averages


def get_player_current_stats(playerid):
    url = stats_endpoint+"?"+"per_page=100&"+"seasons[]="+str(datetime.date.today().year-1)+"&"+"player_ids[]="+str(playerid)
    
    response = requests.request("GET", url)
    data = response.json()
    return data["data"]

def get_list_of_stats(current_stats):
    player_stats = []
    for stat in current_stats:
        try:
            home_team = get_team_name(stat["game"]["home_team_id"])
        except JSONDecodeError:
            home_team = None
        try:
            visitor_team = get_team_name(stat["game"]["visitor_team_id"])
        except JSONDecodeError:
            visitor_team = None
        player = PlayerGameStat()
        player.home_team = home_team
        player.home_team_score = stat["game"]["home_team_score"]
        player.visitor_team = visitor_team
        player.visitor_team_score = stat["game"]["visitor_team_score"] 
        player.min = stat["min"]
        player.pts = stat["pts"]
        player.fg_pct = stat["fg_pct"]
        player.fga = stat["fga"]
        player.fgm = stat["fgm"]
        player.fg3_pct = stat["fg3_pct"]
        player.fg3a = stat["fg3a"]
        player.fg3m = stat["fg3m"]
        player.ft_pct = stat["ft_pct"]
        player.fta = stat["fta"]
        player.ftm = stat["ftm"]
        player.oreb = stat["oreb"]
        player.dreb = stat["dreb"]
        player.reb = stat["reb"]
        player.ast = stat["ast"]
        player.turnover = stat["turnover"]
        player.stl = stat["stl"]
        player.blk = stat["blk"]
        player.pf = stat["pf"]
        player_stats.append(player)
    return player_stats

class PlayerGameStat:
    def __init__(self):
        self.home_team = ""
        self.home_team_score = ""
        self.visitor_team = ""
        self.visitor_team_score = ""
        self.min = ""
        self.pts = ""
        self.fg_pct = ""
        self.fga = ""
        self.fgm = ""
        self.fg3_pct = ""
        self.fg3a = ""
        self.fg3m = ""
        self.ft_pct = ""
        self.fta = ""
        self.ftm = ""
        self.oreb = ""
        self.dreb = ""
        self.reb = ""
        self.ast = ""
        self.turnover = ""
        self.stl = ""
        self.blk = ""
        self.pf = ""

# DATA.NBA.NET functions

def get_player_info(playerid):
    year = datetime.date.today().year
    url = "https://data.nba.net/data/10s/prod/v1/"+str(year)+"/players.json"
    
    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]
    player = [player for player in players if player["personId"] == str(playerid)]

    try:
        return player[0]
    except IndexError:
        return None


def get_player_photo(person_id):
    url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+str(person_id)+".png"
    return url