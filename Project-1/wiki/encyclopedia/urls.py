from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new-entry", views.new_entry, name="new-entry")
]
