from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

import json
import pandas as pd

from .models import User, Player, Bookmark
from .util import get_player_photo, get_player_info, get_season_avgs, get_team_name, get_team_photo
from .util import random_players, search_players


def index(request):
    results = random_players()

    for player_info in results:
        player_info["photo_url"] = get_player_photo(player_info["personId"])

    return render(request, 'nbastats/index.html', {
        'results': results
    })


def search(request):
    query = request.GET.get('q')

    results = search_players(query)
    for player_info in results:
        player_info["photo_url"] = get_player_photo(player_info["personId"])

    return render(request, 'nbastats/search_results.html', {
        'results': results
    })


def player(request, playerid):

    # Get player info
    player_info = get_player_info(playerid)
    # Get photo, team name, and team photo
    player_info["photo_url"] = get_player_photo(playerid)
    player_info["team"] = get_team_name(player_info["teamId"])
    player_info["team_url"] = get_team_photo(player_info["teamId"])

    # Get season averages
    season_averages = get_season_avgs(playerid)
    # Create df and clean
    df = pd.DataFrame(season_averages)
    df.set_index('season', inplace=True, drop=True)
    df.index.name = None
    # Stylize column names
    df.rename(columns={'ppg': 'PPG', 'rpg': 'RPG', 'apg': 'APG', 'mpg': 'MPG', 'topg': 'TOPG',
                       'spg': 'SPG', 'bpg': 'BPG', 'tpp': 'TPP', 'gamesPlayed': 'GP', 'gamesStarted': 'GS',
                       'min': 'MIN', 'fgm': 'FGM', 'fga': 'FGA', 'tpm': '3PM', 'tpa': '3PA',
                       'ftm': 'FTM', 'fta': 'FTA', 'offReb': 'OREB', 'defReb': 'DREB', 'totReb': 'REB',
                       'assists': 'AST', 'steals': 'STL', 'blocks': 'BLK', 'turnovers': 'TOV',
                       'pFouls': 'PF', 'points': 'PTS', 'fgp': 'FG%', 'fg3_pct': '3P%', 'ftp': 'FT%',
                       'plusMinus': '+/-', 'dd2': 'DD2', 'td3': 'TD3'},
              inplace=True)
    # Create HTML table for display
    html = df.to_html(classes="table")

    # Check if user already favorites this
    show_favorite = True
    if (request.user and Player.objects.filter(player_id=playerid)):
        player = Player.objects.get(player_id=playerid)
        Bookmark.objects.filter(user=request.user, player=player)
        show_favorite = False

    return render(request, 'nbastats/player.html', {
        'show_favorite': show_favorite,
        'player_info': player_info,
        'html': html
    })


def user(request, username):
    bookmarks = Bookmark.objects.filter(user=request.user)
    results = []

    # Add player_info to bookmarked players
    for bookmark in bookmarks:
        player_id = bookmark.player.player_id
        player_info = get_player_info(player_id)
        player_info["photo_url"] = get_player_photo(player_id)
        player_info["team"] = get_team_name(player_info["teamId"])
        player_info["team_url"] = get_team_photo(player_info["teamId"])
        results.append(player_info)

    return render(request, "nbastats/user.html", {
        'username': username,
        'results': results
    })


@csrf_exempt
# API endpoints
def bookmark(request):
    if request.method == "PUT":
        # Get user
        user = User.objects.get(username=request.user)
        # Get player to be favorited
        data = json.loads(request.body)
        player_id = data['playerId']
        Player.objects.get_or_create(player_id=int(player_id))
        player = Player.objects.get(player_id=int(player_id))

        if data['favorite']:  # favorite
            Bookmark.objects.get_or_create(user=user, player=player)
        elif not data['favorite']:  # unfavorite
            to_unlike = Bookmark.objects.get(user=user, player=player)
            to_unlike.delete()

        return HttpResponse(200)

    return Http404


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
