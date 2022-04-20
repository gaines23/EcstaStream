# Generated by Django 3.2.6 on 2022-04-20 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20220419_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplaylist',
            name='cover_img',
            field=models.ImageField(default='media/default_playlist.png', null=True, upload_to='cover_images/'),
        ),
        migrations.AlterField(
            model_name='userplaylist',
            name='playlist_follows',
            field=models.ManyToManyField(default=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
