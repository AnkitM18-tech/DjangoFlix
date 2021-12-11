from django.db import models
from django.utils import timezone
# from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import TaggedItem
from django.db.models.signals import pre_save
# Create your models here.
from videos.models import Video
from ratings.models import Rating
from categories.models import Category
from djangoflix.db.models import PublishStateOptions
from django.db.models import Avg,Max,Min
from djangoflix.db.receivers import publish_state_pre_save,unique_slugify_pre_save

class PlayListQuerySet(models.QuerySet):
    def published(self):
        now= timezone.now()
        return self.filter(publish_timestamp__lte = now,state=PublishStateOptions.PUBLISH)

class PlayListManager(models.Manager):
    def get_queryset(self):
        return PlayListQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured_playlists(self):
        return self.get_queryset().filter(type=PlayList.PlayListTypeChoices.PLAYLIST)

class PublishStateOptions(models.TextChoices):
    #CONSTANT = DB_VALUE, USER_DISPLAY_VALUE
    PUBLISH = "PU","Publish"
    DRAFT = "DR","Draft"
    UNLISTED = "UN","Unlisted"
    PRIVATE = "PR","Private"

class PlayList(models.Model):
    class PlayListTypeChoices(models.TextChoices):
        MOVIE="MOV","Movie"
        SHOW = "TVS","TV Show"
        SEASON = "SEA","Season"
        PLAYLIST = "PLY","PlayList"

    parent = models.ForeignKey("self",blank=True,null=True,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,blank=True,null=True,related_name='playlists',on_delete=models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=3,choices=PlayListTypeChoices.choices,default=PlayListTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,null=True)
    video = models.ForeignKey(Video,related_name='playlist_featured',blank=True,null=True,on_delete=models.SET_NULL)   #One Video Per Playlist
    videos = models.ManyToManyField(Video,related_name='playlist_item',blank=True,through="PlayListItem")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices,default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    tags = GenericRelation(TaggedItem,related_query_name='playlist')
    ratings = GenericRelation(Rating,related_query_name='playlist')

    objects = PlayListManager()

    # class Meta:
    #     unique_together = (('title','slug'))

    def __str__(self) :
        return self.title

    def get_rating_average(self):
        return PlayList.objects.filter(id=self.id).aggregate(Avg("ratings__value"))

    def get_rating_spread(self):
        return PlayList.objects.filter(id=self.id).aggregate(max=Max("ratings__value"),min=Min("ratings__value"))

    def get_short_display(self):
        return ""

    @property
    def is_published(self):
        return self.active

    # def save(self,*args,**kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args,**kwargs)

class TVShowProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,type=PlayList.PlayListTypeChoices.SHOW)

class TVShowProxy(PlayList):
    objects = TVShowProxyManager()
    class Meta:
        verbose_name = "TV Show"
        verbose_name_plural = "TV Shows"
        proxy = True
    
    def save(self,*args,**kwargs):
        self.type = PlayList.PlayListTypeChoices.SHOW
        super().save(*args,**kwargs)

    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

class TVShowSeasonProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,type=PlayList.PlayListTypeChoices.SEASON)

class TVShowSeasonProxy(PlayList):
    objects = TVShowSeasonProxyManager()
    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        proxy = True

    def save(self,*args,**kwargs):
        self.type = PlayList.PlayListTypeChoices.SEASON
        super().save(*args,**kwargs)

class MovieProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(type=PlayList.PlayListTypeChoices.MOVIE)

class MovieProxy(PlayList):
    objects = MovieProxyManager()
    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        proxy = True

    def save(self,*args,**kwargs):
        self.type = PlayList.PlayListTypeChoices.MOVIE
        super().save(*args,**kwargs)

class PlayListItem(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['order','-timestamp']

pre_save.connect(publish_state_pre_save,sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowProxy)
pre_save.connect(publish_state_pre_save,sender=PlayList)
pre_save.connect(unique_slugify_pre_save,sender=PlayList)
pre_save.connect(publish_state_pre_save,sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save,sender=MovieProxy)
pre_save.connect(publish_state_pre_save,sender=TVShowSeasonProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowSeasonProxy)