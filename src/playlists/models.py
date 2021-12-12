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
from django.db.models import Avg,Max,Min,Q
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
    related = models.ManyToManyField("self",blank=True,related_name="related",through="PlayListRelated")
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

    def get_related_items(self):
        return self.playlistrelated_set.all()

    def get_rating_average(self):
        return PlayList.objects.filter(id=self.id).aggregate(Avg("ratings__value"))

    def get_rating_spread(self):
        return PlayList.objects.filter(id=self.id).aggregate(max=Max("ratings__value"),min=Min("ratings__value"))

    def get_short_display(self):
        return ""

    def get_absolute_url(self):
        if self.is_movie:
            return f'/movies/{self.slug}/'
        if self.is_show:
            return f'/shows/{self.slug}/'
        if self.is_season and self.parent is not None:
            return f'/shows/{self.parent.slug}/seasons/{self.slug}/'
        return f'/playlists/{self.slug}/'
    

    @property
    def is_published(self):
        return self.active
    @property
    def is_movie(self):
        return self.type == self.PlayListTypeChoices.MOVIE
    @property
    def is_show(self):
        return self.type == self.PlayListTypeChoices.SHOW
    @property
    def is_season(self):
        return self.type == self.PlayListTypeChoices.SEASON

    def get_video_id(self): #get main video id to render videos for users
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):  #get clips to render clips for users
        return self.playlistitem_set.all().published()

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

    def get_episodes(self):  #get episodes to render for users
        return self.playlistitem_set.all().published()

    def get_season_trailer(self):  #get season trailer to render for users
        return self.get_video_id()

class MovieProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(type=PlayList.PlayListTypeChoices.MOVIE)

class MovieProxy(PlayList):
    objects = MovieProxyManager()

    def get_movie_id(self): #get movie id to render movies for users
        return self.get_video_id()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        proxy = True

    def save(self,*args,**kwargs):
        self.type = PlayList.PlayListTypeChoices.MOVIE
        super().save(*args,**kwargs)

class PlayListItemQuerySet(models.QuerySet):
    def published(self):
        now= timezone.now()
        return self.filter(video__publish_timestamp__lte = now,video__state=PublishStateOptions.PUBLISH,playlist__publish_timestamp__lte = now,playlist__state=PublishStateOptions.PUBLISH)

class PlayListItemManager(models.Manager):
    def get_queryset(self):
        return PlayListItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

class PlayListItem(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PlayListItemManager()
    class Meta:
        ordering=['order','-timestamp']

#qs = PlayList.objects.filter(type=PlayList.PlayListTypeChoices.MOVIE)
#qs2 = PlayList.objects.filter(type=PlayList.PlayListTypeChoices.SHOW)
#final_qs = qs | qs2

def pr_limit_choices_to():
    return Q(type=PlayList.PlayListTypeChoices.MOVIE) | Q(type=PlayList.PlayListTypeChoices.SHOW)

class PlayListRelated(models.Model):
    playlist = models.ForeignKey(PlayList,on_delete=models.CASCADE)
    related  = models.ForeignKey(PlayList,on_delete=models.CASCADE, related_name="related_item",limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

pre_save.connect(publish_state_pre_save,sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowProxy)
pre_save.connect(publish_state_pre_save,sender=PlayList)
pre_save.connect(unique_slugify_pre_save,sender=PlayList)
pre_save.connect(publish_state_pre_save,sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save,sender=MovieProxy)
pre_save.connect(publish_state_pre_save,sender=TVShowSeasonProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowSeasonProxy)