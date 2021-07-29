import json

from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count

from .models import User, Post, Follow, Like

# HELPER FUNCTIONS
def get_page(request, posts):
    page_number = request.GET.get('page', 1) # 1 is default
    paginator = Paginator(posts, 10)
    page = paginator.page(page_number)
    return page

def get_following_posts(request):
    viewer = User.objects.get(username=request.user)
    users_followed = [following.target for following in Follow.objects.filter(follower=viewer)]
    posts = [Post.objects.annotate(num_likes=Count('likes')).filter(author=user) for user in users_followed]
    flat_list = [post for queryset in posts for post in queryset]
    posts = sorted(flat_list, key=lambda post: post.created_on, reverse=True)

    return posts

def get_post_likes(request, posts):
    # Annotate Post objects for displaying on HTML page
    if request.user.is_anonymous:
        for post in posts:
            post.like = False
    else:
        for post in posts:
            post.like = post.does_user_like(user=request.user)

    return posts

def send_post(request, post_form):
    # Check form is valid
    if post_form.is_valid():
        post = post_form.save(commit=False)

        # Update and save new post on listing
        post.author = request.user
        post.save()
        
        return True
    return False

def send_like_edit_post(request):
    data = json.loads(request.body)
    post_id = data['id']
    post = Post.objects.get(pk=post_id)

    if 'text' in data:
        post_text = data['text']
        post.text = post_text
        post.save()
    else:
        if data['like']:
            Like.objects.get_or_create(user=request.user, post=post)
        elif not data['like']:
            to_unlike = Like.objects.get(user=request.user, post=post)
            to_unlike.delete()

def send_follow(request, viewer, viewee):
    value = request.POST.get("Follow")

    if value == "Follow":
        Follow.objects.get_or_create(target=viewee, follower=viewer)
        return True
    elif value == "Unfollow":
        Follow.objects.filter(target=viewee, follower=viewer).delete()
        return True
    else:
        return False