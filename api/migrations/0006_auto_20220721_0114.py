# Generated by Django 3.2.13 on 2022-07-21 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_content_comment_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Boring'), (2, 'Normal'), (3, 'Biased'), (4, 'Somewhat Interesting'), (5, 'Interesting')], default=1)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chapter')),
            ],
        ),
    ]