# Generated by Django 3.2.13 on 2022-07-21 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_like_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='ch_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]
