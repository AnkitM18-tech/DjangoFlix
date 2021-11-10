from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField()
    description = models.TextField()
    slug = models.SlugField(blank=True,null=True) #This is my video
    video_id = models.CharField()
    # timestamp
    # updated
    # state
    # publish_timestamp 