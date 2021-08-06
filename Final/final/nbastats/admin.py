from django.contrib import admin

from .models import User, Player, Bookmark

# Register your models here.

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Bookmark)
