# from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.http import Http404
from django.utils import timezone
from djangoflix.db.models import PublishStateOptions
# Create your views here.
from .models import MovieProxy,TVShowProxy,PlayList,TVShowSeasonProxy

class PlayListMixin():
    title = None
    template_name = "playlist_list.html"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context["title"] = self.title
        print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().published()

class MovieListView(PlayListMixin,ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

class MovieDetailView(PlayListMixin,DetailView):
    template_name = "playlists/movie_detail.html"
    queryset = MovieProxy.objects.all()

class PlayListDetailView(PlayListMixin,DetailView):
    template_name = "playlists/playlist_detail.html"
    queryset = PlayList.objects.all()

class TVShowListView(PlayListMixin,ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV Shows"

class TVShowDetailView(PlayListMixin,DetailView):
    template_name = "playlists/tvshow_detail.html"
    queryset = TVShowProxy.objects.all()

class TVShowSeasonDetailView(PlayListMixin,DetailView):
    template_name = "playlists/season_detail.html"
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug,
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug,
            ).published()
            obj = qs.first()

        except:
            raise Http404
        return obj
        # qs  =self.get_queryset().filter(parent__slug__iexact=show_slug,slug__iexact=season_slug)
        # if not qs.count() == 1:
        #     raise Http404
        # return qs.first()

class FeaturedPlayListListView(PlayListMixin,ListView):
    template_name = "playlists/featured_list.html"
    queryset = PlayList.objects.featured_playlists()
    title = "Featured"