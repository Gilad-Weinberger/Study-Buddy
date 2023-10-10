from django.db import models
from django.contrib.auth.models import AbstractUser
import os

def profile_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"profile_{instance.email}{ext}"
    return os.path.join('profile_images', new_filename)

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []