from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'{self.user}: {self.post}'


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.text} \n Created on: {self.created_on}'

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "created_on": self.created_on
        }

    def does_user_like(self, user):
        if Like.objects.filter(user=user, post=self).exists():
            return True
        return False


class Follow(models.Model):
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="targets")

    def __str__(self):
        return f'target: {self.target}, follower: {self.follower}'
