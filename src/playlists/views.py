# from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from .models import MovieProxy,TVShowProxy,PlayList

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

class TVShowListView(PlayListMixin,ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV Shows"

class FeaturedPlayListListView(PlayListMixin,ListView):
    # template_name = "featured_playlist_list.html"
    queryset = PlayList.objects.featured_playlists()
    title = "Featured"