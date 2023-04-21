from django.contrib import admin

from social_media.models import UserProfile, Post

admin.site.register(UserProfile)

admin.site.register(Post)
