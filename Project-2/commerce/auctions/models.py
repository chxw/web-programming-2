import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    # categories = models.TextChoices('Fashion', 'Toys', 'Electronics', 'Home')
    title = models.CharField(max_length=30)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    image = models.URLField(blank=True)
    # category = models.CharField(blank=True, max_length=10, choices=categories.choices)

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass