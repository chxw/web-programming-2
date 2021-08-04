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
from .util import get_list_of_stats, get_player_NBAID, get_player_current_stats, get_player_photo, get_players, get_season_averages, get_team_name, get_player_info, get_page, PlayerGameStat


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

    results = get_players(query)

    return render(request, 'nbastats/index.html', {
        'results': results
    })

def player(request, playerid):

    # Get player info
    player_info = get_player_info(playerid)
    fname = player_info['first_name']
    lname = player_info['last_name']

    # Get photo
    NBA_id = get_player_NBAID(fname=fname, lname=lname)
    photo_url = get_player_photo(NBA_id)

    # # Get season averages
    # season_averages = get_season_averages(playerid)
    # df = pd.DataFrame.from_dict(season_averages)
    # df.set_index('season', inplace=True, drop=True)
    # df.index.name=None
    # df.drop(columns='player_id', inplace=True)
    # df.rename(columns={'games_played':'GP', 'min':'MIN', 'fgm':'FGM', 'fga':'FGA', 'fg3m':'3PM', 'fg3a':'3PA', 'ftm':'FTM', 'fta':'FTA', 'oreb':'OREB', 'dreb':'DREB', 'reb':'REB', 'ast':'AST', 'stl':'STL', 'blk':'BLK', 'turnover':'TOV', 'pf':'PF', 'pts':'PTS', 'fg_pct':'FG%', 'fg3_pct':'3P%', 'ft_pct':'FT%'},inplace=True)
    # html = df.to_html(classes="table")

    return render(request, 'nbastats/player.html', {
        'fname': fname,
        'lname': lname,
        'player_info': player_info,
        # 'current_stats': player_stats,
        'photo_url': photo_url,
        # 'html': html
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
