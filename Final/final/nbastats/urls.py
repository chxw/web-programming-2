from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("player/<int:playerid>", views.player, name="player"),
    path("bookmark", views.bookmark, name="bookmark"),
    path("user/<str:username>", views.user, name="user")
]
