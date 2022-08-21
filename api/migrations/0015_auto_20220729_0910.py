# Generated by Django 3.2.13 on 2022-07-29 08:10

import cloudinary.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_auto_20220729_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='id',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='following',
            name='id',
        ),
        migrations.RemoveField(
            model_name='following',
            name='profile',
        ),
        migrations.AddField(
            model_name='follower',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 7, 29, 8, 9, 9, 308184, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='follower',
            name='follin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='api.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='follower',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='follower',
            name='read_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='follower',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='follower',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='following',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='following',
            name='foller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followings', to='api.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='following',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='following',
            name='read_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='following',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='following',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user'),
            preserve_default=False,
        ),
    ]
