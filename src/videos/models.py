from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class VideoQuerySet(models.QuerySet):
    def published(self):
        now= timezone.now()
        return self.filter(publish_timestamp__lte = now,state=Video.VideoStateOptions.PUBLISH)

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    # def published(self):
    #     return self.get_queryset().published()

class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        #CONSTANT = DB_VALUE, USER_DISPLAY_VALUE
        PUBLISH = "PU","Publish"
        DRAFT = "DR","Draft"
        UNLISTED = "UN","Unlisted"
        PRIVATE = "PR","Private"


    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,null=True) #This is my video
    video_id = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices,default=VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active

    def save(self,*args,**kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            # print("Saved as timestamp for published!")
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:
            self.publish_timestamp = None
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)

class VideoPublishedProxy(Video):
    class Meta:
        proxy=True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'

class VideoAllProxy(Video):
    class Meta:
        proxy=True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'
