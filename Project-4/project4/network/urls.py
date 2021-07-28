
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user, name="user"),
    path("following", views.following, name="following"),
    path("api/posts/<int:id>", views.posts, name="posts"),
    path("api/likes/<int:id>", views.likes, name="likes")
]
