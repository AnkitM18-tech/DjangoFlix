# Generated by Django 3.2.9 on 2021-11-12 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20211113_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
