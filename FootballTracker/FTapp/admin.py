# Register your models here.
from django.contrib import admin
from .models import UserProfile, PlayerProfile, Post, Message

admin.site.register(UserProfile)
admin.site.register(PlayerProfile)
admin.site.register(Post)
admin.site.register(Message)
