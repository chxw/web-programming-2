from json.decoder import JSONDecodeError

from requests.api import get
from final.settings import RAPID_API_KEY
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

import requests
import json
import datetime

from .models import User
from .util import get_player_NBAID, get_player_photo, get_team_name, PlayerGameStat

# Create your views here.

players_endpoint = "https://www.balldontlie.io/api/v1/players/"
stats_endpoint = "https://www.balldontlie.io/api/v1/stats/"

def index(request):

    url = "https://nba-stats4.p.rapidapi.com/players/"

    querystring = {"page":"1","per_page":"50"}

    headers = {
        'x-rapidapi-key': RAPID_API_KEY,
        'x-rapidapi-host': "nba-stats4.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return render(request, 'nbastats/index.html')

def player(request, playerid):

    # Player info
    url = players_endpoint+str(playerid)

    response = requests.request("GET", url)
    player_info = response.json()
    fname = player_info['first_name']
    lname = player_info['last_name']
    NBA_id = get_player_NBAID(fname=fname, lname=lname)
    photo_url = get_player_photo(NBA_id)

    # # Full stats
    # url = stats_endpoint+"?"+"player_ids[]="+str(playerid)
    
    # response = requests.request("GET", url)
    # data = response.json()
    # full_stats = data["data"]

    # Current stats
    url = stats_endpoint+"?"+"per_page=100&"+"seasons[]="+str(datetime.date.today().year-1)+"&"+"player_ids[]="+str(playerid)
    
    response = requests.request("GET", url)
    data = response.json()
    current_stats = data["data"]

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


    return render(request, 'nbastats/player.html', {
        'fname': fname,
        'lname': lname,
        'height_ft': player_info['height_feet'],
        'height_in': player_info['height_inches'],
        'position': player_info['position'],
        'team': player_info['team']['full_name'],
        # 'full_stats': full_stats,
        'current_stats': player_stats,
        'photo_url': photo_url
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
