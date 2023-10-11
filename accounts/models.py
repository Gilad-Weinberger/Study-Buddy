from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.contrib.auth.models import BaseUserManager

def profile_image_upload_path(instance, filename):
    if instance.avatar:
        instance.avatar.delete()

    filename, ext = os.path.splitext(filename)
    new_filename = f"profile_{instance.username}{ext}"
    return os.path.join('profile_images', new_filename)


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(
        null=True,
        upload_to=profile_image_upload_path,
        default='profile_images/default.png' 
    )
    about = models.TextField(null=True, max_length=300)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []