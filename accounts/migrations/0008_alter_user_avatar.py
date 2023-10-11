# Generated by Django 4.2.4 on 2023-10-10 10:57

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='profile_images/default.png', null=True, upload_to=accounts.models.profile_image_upload_path),
        ),
    ]