from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new-entry", views.new_entry, name="new-entry"),
    path("wiki/edit/<str:title>", views.edit_entry, name="edit-entry"),
    path("404", views.handler404, name="404")
]
