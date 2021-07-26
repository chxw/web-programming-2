from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like
from .forms import PostForm

def render_with_paginator(request, posts):
    page_number = request.GET.get('page', 1) # 1 is default
    paginator = Paginator(posts, 10)
    page = paginator.page(page_number)
    return render(request, "marketplace/index.html", {'page': page})


def handle_post(request):
    # Post on listing
    if request.POST.get("Post"):
        # Save text as instance of Post model
        post_form = PostForm(request.POST)

        # Check form is valid
        if post_form.is_valid():
            post = post_form.save(commit=False)

            # Update and save new post on listing
            post.author = request.user
            post.save()

            return redirect(reverse("index"))

def index(request):
    handle_post(request)

    page_number = request.GET.get('page', 1)
    pages = Paginator(Post.objects.order_by('-created_on'), 10)
    page = pages.page(page_number)

    return render(request, "network/index.html", {
        'post_form': PostForm(),
        'page': page
    })

def following(request):
    handle_post(request)

    viewer = User.objects.get(username=request.user)
    users_followed = [following.target for following in Follow.objects.filter(follower=viewer)]
    posts = [Post.objects.filter(author=user) for user in users_followed]
    flat_list = [post for queryset in posts for post in queryset]
    posts_sorted = sorted(flat_list, key=lambda post: post.created_on, reverse=True)
    pages = Paginator(posts_sorted, 10)

    return render(request, "network/index.html", {
        'post_form': PostForm(),
        'posts': pages.page(1)
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user(request, username):
    # Does request.user follow username?
    viewer = User.objects.get(username=request.user)
    viewee = User.objects.get(username=username)

    # Follow user
    if request.POST.get("Follow") == "Follow":
        Follow.objects.get_or_create(target=viewee, follower=viewer)

    elif request.POST.get("Follow") == "Unfollow":
        Follow.objects.filter(target=viewee, follower=viewer).delete()

    return render(request, "network/user.html", {
        'username': username,
        'posts': Post.objects.filter(author=User.objects.get(username=username)).order_by('-created_on'),
        'following' : Follow.objects.filter(target=viewee, follower=viewer).exists(),
        'num_followers': Follow.objects.filter(target=viewee).count(),
        'num_following': Follow.objects.filter(follower=viewee).count
    })