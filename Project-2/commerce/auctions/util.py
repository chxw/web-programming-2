from .models import Watchlist


def check_watchlist(listing, user):
    for item in Watchlist.objects.filter(watcher=user):
        if item.listing.id == listing.id:
            return True
    return False
