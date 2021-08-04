# Importing the necessary libraries
import requests
import pandas as pd

# Under the Header tab, select general and copy the first part of the request URL
url = 'https://stats.nba.com/stats/playergamelogs'

#Header Tab, under "Query String Parameter" subsection
params =(
("DateTo", ""),
("GameSegment", ""),
("LastNGames", "0"),
("LeagueID", "00"),
("Location", ""),
("MeasureType", "Base"),
("Month", "0"),
("OpponentTeamID", "0"),
("Outcome", ""),
("PORound", "0"),
("PaceAdjust", "N"),
("PerMode", "Totals"),
("Period", "0"),
("PlusMinus", "N"),
("Rank", "N"),
("Season", "2020-21"),
("SeasonSegment", ""),
("SeasonType", "Regular Season"),
("ShotClockRange", ""),
("VsConference", ""),
("VsDivision", "" ))

# Header tab, under “Request Headers” subsection
header = {
"accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0.9",
"origin": "https://www.nba.com",
"referer": "https://www.nba.com/",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
"x-nba-stats-origin": "stats",
"x-nba-stats-token": "true"}

# #Using Request library to get the data
# response = requests.get(url, headers=header, params=params)
# response_json = response.json()
# frame = pd.DataFrame(response_json['resultSets'][0]['rowSet'])
# frame.columns = response_json['resultSets'][0]['headers']
# print(frame.head())

print("here")