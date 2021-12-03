from django.db import models
from django.utils import timezone
# from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
from videos.models import Video
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save,slugify_pre_save

class PlayListQuerySet(models.QuerySet):
    def published(self):
        now= timezone.now()
        return self.filter(publish_timestamp__lte = now,state=PublishStateOptions.PUBLISH)

class PlayListManager(models.Manager):
    def get_queryset(self):
        return PlayListQuerySet(self.model, using=self._db)

    # def published(self):
    #     return self.get_queryset().published()

class PublishStateOptions(models.TextChoices):
    #CONSTANT = DB_VALUE, USER_DISPLAY_VALUE
    PUBLISH = "PU","Publish"
    DRAFT = "DR","Draft"
    UNLISTED = "UN","Unlisted"
    PRIVATE = "PR","Private"

class PlayList(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,null=True)
    video = models.ForeignKey(Video,related_name='playlist_featured',null=True,on_delete=models.SET_NULL)   #One Video Per Playlist
    videos = models.ManyToManyField(Video,related_name='playlist_item',blank=True,through="PlayListItem")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

    objects = PlayListManager()

    @property
    def is_published(self):
        return self.active

    # def save(self,*args,**kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args,**kwargs)

pre_save.connect(publish_state_pre_save,sender=PlayList)
pre_save.connect(slugify_pre_save,sender=PlayList)

class PlayListItem(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['order','-timestamp']