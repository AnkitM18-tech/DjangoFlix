from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,null=True) #This is my video
    video_id = models.CharField(max_length=200)
    # timestamp
    # updated
    # state
    # publish_timestamp 