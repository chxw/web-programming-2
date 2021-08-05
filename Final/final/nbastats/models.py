from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Player(models.Model):
    player_id = models.IntegerField()

class Bookmark():
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookmarks")
    player = models.ForeignKey(
        'Player', on_delete=models.CASCADE, related_name="bookmarks")