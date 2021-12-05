# Generated by Django 3.2.9 on 2021-12-05 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_alter_video_video_id'),
        ('playlists', '0008_tvshowproxy_tvshowseasonproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='type',
            field=models.CharField(choices=[('MOV', 'Movie'), ('TVS', 'TV Show'), ('SEA', 'Season'), ('PLY', 'PlayList')], default='PLY', max_length=3),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='playlist_featured', to='videos.video'),
        ),
    ]