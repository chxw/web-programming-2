from typing import get_args
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watched_listings = models.ManyToManyField(
        'Listing', related_name="watchers", blank=True)


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True, null=True)


class Listing(models.Model):
    owner = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=30)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    image = models.URLField(blank=True, null=True)
    current_price = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.CASCADE, related_name="listings")

    def _get_last_bid(self):
        qs = Bid.objects.filter(listing=self).order_by('-created_on')
        last_bids = [(item.bidder, item.bid) for item in qs]
        if len(last_bids) != 0:
            return last_bids[0]
        else:
            return None

    def winner(self):
        bid = self._get_last_bid()
        if bid:
            return bid[0]  # return bidder
        return None

    def winning_bid(self):
        bid = self._get_last_bid()
        if bid:
            return bid[1]  # return bid price
        return None

    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.starting_bid
        return super(Listing, self).save(*args, **kwargs)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="bids")
    bid = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now=True)


class Watchlist(models.Model):
    watcher = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, null=True, on_delete=models.CASCADE, related_name="watchlist")

    class Meta:
        unique_together = ["watcher", "listing"]
