from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.text}'

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "created_on": self.created_on
        }
    
    def does_user_like(self, user):
        return Like.objects.filter(post=self, user=user).exists()

class Follow(models.Model):
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")    
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="targets")

    def __str__(self):
        return f'target: {self.target}, follower: {self.follower}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ["user", "post"]