# Generated by Django 3.2.9 on 2021-12-12 10:07

from django.db import migrations, models
import django.db.models.deletion
import playlists.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0014_auto_20211212_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistrelated',
            name='related',
            field=models.ForeignKey(limit_choices_to=playlists.models.pr_limit_choices_to, on_delete=django.db.models.deletion.CASCADE, related_name='related_item', to='playlists.playlist'),
        ),
    ]
