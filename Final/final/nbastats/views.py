from requests.api import get
from final.settings import RAPID_API_KEY
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

import requests
import pandas as pd

from .models import User
from .util import get_list_of_stats, get_player_current_stats, get_player_photo, get_players, get_team_name, get_player_info, get_page, PlayerGameStat, get_season_avgs, search_players


# # Get current stats
# current_stats = get_player_current_stats(playerid)
# player_stats = get_list_of_stats(current_stats)


def index(request):

    # url = "https://nba-stats4.p.rapidapi.com/players/"

    # querystring = {"page":"1","per_page":"50"}

    # headers = {
    #     'x-rapidapi-key': RAPID_API_KEY,
    #     'x-rapidapi-host': "nba-stats4.p.rapidapi.com"
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    return render(request, 'nbastats/index.html')

def search(request):
    query = request.GET.get('q')

    results = search_players(query)

    return render(request, 'nbastats/search_results.html', {
        'results': results
    })

def player(request, playerid):

    # Get player info
    player_info = get_player_info(playerid)
    # Get photo
    photo_url = get_player_photo(playerid)

    # Get season averages
    season_averages = get_season_avgs(playerid)
    # Create df and clean
    df = pd.DataFrame(season_averages)
    df.set_index('season', inplace=True, drop=True)
    df.index.name=None
    df.rename(columns={'ppg':'PPG', 'rpg':'RPG', 'apg':'APG', 'mpg':'MPG', 'topg':'TOPG', 'spg':'SPG', 'bpg':'BPG', 'tpp':'TPP', 'gamesPlayed':'GP', 'gamesStarted':'GS', 'min':'MIN', 'fgm':'FGM', 'fga':'FGA', 'tpm':'3PM', 'tpa':'3PA', 'ftm':'FTM', 'fta':'FTA', 'offReb':'OREB', 'defReb':'DREB', 'totReb':'REB', 'assists':'AST', 'steals':'STL', 'blocks':'BLK', 'turnovers':'TOV', 'pFouls':'PF', 'points':'PTS', 'fgp':'FG%', 'fg3_pct':'3P%', 'ftp':'FT%', 'plusMinus':'+/-', 'dd2':'DD2', 'td3':'TD3'},inplace=True)
    # Create HTML table for display
    html = df.to_html(classes="table")

    return render(request, 'nbastats/player.html', {
        'player_info': player_info,
        'photo_url': photo_url,
        'html': html
    })

# Login / Logout / Register

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "nbastats/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "nbastats/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "nbastats/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "nbastats/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "nbastats/register.html")
