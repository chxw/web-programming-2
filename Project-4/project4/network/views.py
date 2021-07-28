from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from .models import User, Post, Follow, Like
from .forms import PostForm
from .util import get_page, send_post, send_like_edit_post, get_following_posts, get_post_likes, send_follow

@csrf_exempt
def index(request):
    # Initialize variables
    post_form = PostForm()
    posts = []

    # User POSTS something
    if request.POST.get("Post"):
        # Save text as instance of Post model
        post_form = PostForm(request.POST)

        if (send_post(request, post_form)):
            return redirect(request.path_info)
        return HttpResponse(status=400)

    # User LIKES something
    elif request.method == "PUT":
        send_like_edit_post(request)

    if request.path_info == '/':
        # Grab and format ALL posts
        posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-created_on')
        posts = get_post_likes(request, posts)
    elif request.path_info == '/following': 
        # Grab and format FOLLOWING posts
        posts = get_following_posts(request)
        posts = get_post_likes(request, posts)

    return render(request, "network/index.html", {
        'post_form': post_form,
        'page': get_page(request, posts)
    })

@csrf_exempt
def user(request, username):
    # Grab necessary info
    viewer = User.objects.get(username=request.user)
    viewee = User.objects.get(username=username)
    following = Follow.objects.filter(target=viewee, follower=viewer).exists() # True or False
    num_followers = Follow.objects.filter(target=viewee).count() # Number
    num_following = Follow.objects.filter(follower=viewee).count # Number

    # User (UN)FOLLOWS user
    if request.POST.get("Follow"):
        send_follow(request, viewer, viewee)

    # User LIKES or EDITS a post
    elif request.method == "PUT":
        send_like_edit_post(request)

    # Grab and format posts
    posts = Post.objects.annotate(num_likes=Count('likes')).filter(author=User.objects.get(username=username)).order_by('-created_on')
    posts = get_post_likes(request, posts)

    return render(request, "network/index.html", {
        'username': username,
        'page': get_page(request, posts),
        'following' : following,
        'num_followers': num_followers,
        'num_following': num_following
    })

### API endpoints
def posts(request, id):
    """
    Returns serialized Post object based on post id (id). 

    Located at: api/posts/<int:id>. 
    """
    post = Post.objects.get(pk=id)
    return JsonResponse(post.serialize(), safe=False)

def likes(request, id):
    """
    Returns number of likes on a post based on post id (id). 

    Located at: api/likes/<int:id>. 
    """
    num_likes = Like.objects.filter(post=id).count()
    return JsonResponse(num_likes, safe=False)

### Pre-written views
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