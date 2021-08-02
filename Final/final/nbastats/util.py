import requests

teams_endpoint = "https://www.balldontlie.io/api/v1/teams/"

def get_team_name(id):
    url = teams_endpoint+str(id)

    response = requests.request("GET", url)
    data = response.json()
    return(data["full_name"])

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