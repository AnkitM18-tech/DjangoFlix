# Generated by Django 3.2.9 on 2021-11-11 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_video_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoAllProxy',
            fields=[
            ],
            options={
                'verbose_name': 'All Video',
                'verbose_name_plural': 'All Videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
    ]
