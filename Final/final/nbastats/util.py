import requests
import datetime

teams_endpoint = "https://www.balldontlie.io/api/v1/teams/"

def get_team_name(id):
    url = teams_endpoint+str(id)

    response = requests.request("GET", url)
    data = response.json()
    return(data["full_name"])

def get_player_NBAID(fname, lname):
    year = datetime.date.today().year
    url = "https://data.nba.net/data/10s/prod/v1/"+str(year)+"/players.json"
    
    response = requests.request("GET", url)
    data = response.json()
    players = data["league"]["standard"]
    NBAid = [player["personId"] for player in players if player["firstName"] == fname and player["lastName"] == lname]
    return NBAid[0]

def get_player_photo(person_id):
    url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+str(person_id)+".png"
    return url

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