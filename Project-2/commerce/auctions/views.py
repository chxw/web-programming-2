from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing
from .forms import ListingForm, BidForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
        form = ListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)

            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()

    return render(request, 'auctions/create.html', {'form': form})

def listing(request, id):
    # Get Listing object of current listing page
    listing = Listing.objects.get(id=id)

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)

            # Check bid is valid
            if listing.current_price >= bid.bid:
                messages.error(request, 'Your bid must be larger than current bid.')
                return redirect(reverse('listing', kwargs={'id': id}))

            # Update and save bid instance
            bid.user = request.user
            bid.listing = listing
            bid.save()
            
            # Update and save listing instance
            listing.update_price()
            listing.save()

            return HttpResponseRedirect(reverse("index"))

    else:
        form = BidForm()

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'form': form
        })