# Generated by Django 3.2.13 on 2022-07-29 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20220729_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='follin',
            new_name='who',
        ),
        migrations.RenameField(
            model_name='following',
            old_name='foller',
            new_name='who',
        ),
    ]
