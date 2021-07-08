from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    image = models.URLField(blank=True, null=True)
    current_price = models.PositiveIntegerField(blank=True, null=True)
    
    # categories = models.TextChoices('Fashion', 'Toys', 'Electronics', 'Home')
    # category = models.CharField(blank=True, max_length=10, choices=categories.choices)

    def update_price(self):
        qs = Bid.objects.filter(listing=self).order_by('-bid_time')
        bids = [item.bid for item in qs]
        self.current_price = bids[0]

    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.starting_bid
        return super(Listing, self).save(*args, **kwargs)

class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bid = models.PositiveIntegerField(blank=True, null=True)
    bid_time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)

class Comment(models.Model):
    pass

class Wishlist(models.Model):
    pass