from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:id>", views.categories_active, name="categories-active"),
    path("watchlist", views.watchlist, name="watchlist")
]
