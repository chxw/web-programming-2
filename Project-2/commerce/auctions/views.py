from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Category, Listing, Comment, Watchlist
from .forms import ListingForm, BidForm, CommentForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == 'POST':
        # Does category exist?
        try:
            category = Category(category=request.POST.get('category'))
            category.save()
        # If not, create new category
        except IntegrityError:
            category = Category.objects.get(category=request.POST.get('category'))
        
        # Get user submitted listing
        form = ListingForm(request.POST)
        if form.is_valid():
            # Update user and category for listing, then save
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.category = category
            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, 'auctions/create.html', {'form': form})


def listing(request, id):
    # Initialize variables
    bid_form = None
    comment_form = None
    listing = Listing.objects.get(id=id)

    if request.method == 'POST':
        # Bid on listing
        if request.POST.get("Bid"):
            bid_form = BidForm(request.POST)
            # Check form is valid
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)

                # Check bid is valid
                if listing.current_price >= bid.bid:
                    messages.error(request, 'Your bid must be larger than current bid.')
                    return redirect(reverse('listing', kwargs={'id': id}))

                # Check if user is bidding on own item
                if listing.owner == request.user:
                    messages.error(request, 'You cannot bid on your own item.')
                    return redirect(reverse('listing', kwargs={'id': id}))

                # Update and save new bid on listing
                bid.bidder = request.user
                bid.listing = listing
                bid.save()
                
                # Update and save this page's listing
                listing.current_price = bid.bid
                listing.save()

                return redirect(reverse('listing', kwargs={'id': id}))
        # Close auction
        elif request.POST.get("Close"):
            listing.is_active = False
            listing.save()
            return redirect(reverse('listing', kwargs={'id': id}))
        # Comment on listing
        elif request.POST.get("Comment"):
            comment_form = CommentForm(request.POST)

             # Check form is valid
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)

                # Update and save new comment on listing
                comment.author = request.user
                comment.listing = listing
                comment.save()

                return redirect(reverse('listing', kwargs={'id': id}))
        # Add to/remove from watchlist
        elif request.POST.get("Watchlist"):
            for item in Watchlist.objects.filter(watcher=request.user):
                # If listing already on watchlist, remove from watchlist
                if item.listing.id == listing.id:
                    Watchlist.objects.get(id=item.id).delete()
                    messages.error(request, 'Item removed from watchlist.')
                    return redirect(reverse('listing', kwargs={'id': id}))
            # If listing not on watchlist, add to watchlist
            watchlist = Watchlist(watcher=request.user, listing=listing)
            watchlist.save()
            return redirect(reverse('listing', kwargs={'id': id}))
    else:
        bid_form = BidForm()
        comment_form = CommentForm()

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': Comment.objects.filter(listing=listing)
        })


def categories(request):
    # Filter active categories
    categories = [listing.category for listing in Listing.objects.filter(is_active=True)]
    # Remove duplicate categories
    categories = set(categories)
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


def categories_active(request, id):
    # Filter active listings associated with category id (id)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=id, is_active=True)
    })


def watchlist(request):
    # Filter current user's watchlist 
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(watcher=request.user)
    })
