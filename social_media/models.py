import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=user_image_file_path)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
