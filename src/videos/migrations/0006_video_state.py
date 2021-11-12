# Generated by Django 3.2.9 on 2021-11-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20211112_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='state',
            field=models.CharField(choices=[('PU', 'Publish'), ('DR', 'Draft'), ('UN', 'Unlisted'), ('PR', 'Private')], default='DR', max_length=2),
        ),
    ]