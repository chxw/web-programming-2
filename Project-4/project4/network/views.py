import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


from .models import User, Post, Follow, Like
from .forms import PostForm


def get_page(request, posts):
    page_number = request.GET.get('page', 1) # 1 is default
    paginator = Paginator(posts, 10)
    page = paginator.page(page_number)
    return page

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

    if request.method == "PUT":
        data = json.loads(request.body)

        if 'text' in data:
            data = json.loads(request.body)
            post_id = data['id']
            post_text = data['text']
            post = Post.objects.get(pk=post_id)
            post.text = post_text
            post.save()
        else:
            if 'like' in data:
                data = json.loads(request.body)
                post_id = data['id']
                post = Post.objects.get(pk=post_id)
                Like.objects.get_or_create(user=request.user, post=post)
            else:
                data = json.loads(request.body)
                post_id = data['id']
                post = Post.objects.get(pk=post_id)
                to_unlike = Like.objects.get(user=request.user, post=post)
                to_unlike.delete()


@csrf_exempt
def index(request):
    posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-created_on')
    
    for post in posts:
        post.like = post.does_user_like(user=request.user)
        print('post.like: ', post.like)

    handle_post(request)

    return render(request, "network/index.html", {
        'post_form': PostForm(),
        'page': get_page(request, posts)
    })

def posts(request, id):
    post = Post.objects.get(pk=id)
    return JsonResponse(post.serialize(), safe=False)

def following(request):
    handle_post(request)

    viewer = User.objects.get(username=request.user)
    users_followed = [following.target for following in Follow.objects.filter(follower=viewer)]
    posts = [Post.objects.filter(author=user) for user in users_followed]
    flat_list = [post for queryset in posts for post in queryset]
    posts_sorted = sorted(flat_list, key=lambda post: post.created_on, reverse=True)

    return render(request, "network/index.html", {
        'post_form': PostForm(),
        'page': get_page(request, posts_sorted)
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
    viewer = User.objects.get(username=request.user)
    viewee = User.objects.get(username=username)

    if request.POST.get("Follow") == "Follow":
        Follow.objects.get_or_create(target=viewee, follower=viewer)

    elif request.POST.get("Follow") == "Unfollow":
        Follow.objects.filter(target=viewee, follower=viewer).delete()

    return render(request, "network/user.html", {
        'username': username,
        'page': get_page(request, Post.objects.filter(author=User.objects.get(username=username)).order_by('-created_on')),
        'following' : Follow.objects.filter(target=viewee, follower=viewer).exists(),
        'num_followers': Follow.objects.filter(target=viewee).count(),
        'num_following': Follow.objects.filter(follower=viewee).count
    })