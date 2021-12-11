from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save,slugify_pre_save

class VideoQuerySet(models.QuerySet):
    def published(self):
        now= timezone.now()
        return self.filter(publish_timestamp__lte = now,state=PublishStateOptions.PUBLISH)

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    # def published(self):
    #     return self.get_queryset().published()

class PublishStateOptions(models.TextChoices):
    #CONSTANT = DB_VALUE, USER_DISPLAY_VALUE
    PUBLISH = "PU","Publish"
    DRAFT = "DR","Draft"
    UNLISTED = "UN","Unlisted"
    PRIVATE = "PR","Private"

class Video(models.Model):
    # VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,null=True) #This is my video
    video_id = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

    objects = VideoManager()

    def get_video_id(self):
        if not self.is_published:
            return None
        return self.video_id

    @property
    def is_published(self):
        if self.active is False:
            return False
        state = self.state
        if state != PublishStateOptions.PUBLISH:
            return False
        pub_timestamp = self.publish_timestamp
        if pub_timestamp is None:
            return False
        now = timezone.now()
        return pub_timestamp <= now

    def get_playlist_ids(self):
        #self.<foreign_obj>_set.all()
        return list(self.playlist_featured.all().values_list('id',flat=True))

    # def save(self,*args,**kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args,**kwargs)

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

pre_save.connect(publish_state_pre_save,sender=Video)
pre_save.connect(slugify_pre_save,sender=Video)

pre_save.connect(publish_state_pre_save,sender=VideoPublishedProxy)
pre_save.connect(slugify_pre_save,sender=VideoPublishedProxy)

pre_save.connect(publish_state_pre_save,sender=VideoAllProxy)
pre_save.connect(slugify_pre_save,sender=VideoAllProxy)