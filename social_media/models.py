import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.user)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profiles/", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=user_image_file_path)
    bio = models.TextField(null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', null=True)


    def __str__(self) -> str:
        return f"{self.user}"


class Post(models.Model):
    title = models.CharField(max_length=63, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)

    @property
    def likes(self):
        return self.liked_by.all().count()

    def __str__(self):
        return self.title

