from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from djongo.storage import GridFSStorage

grid_fs_storage = GridFSStorage(collection='Study_Buddy_coll', base_url=''.join([settings.BASE_URL, '']))

class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_images',
        storage=grid_fs_storage
    )
    about = models.TextField(null=True, max_length=300)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []