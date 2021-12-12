from django.views import View
from .models import TaggedItem
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView,DetailView
from django.db.models import Count
from playlists.models import PlayList
from playlists.mixins import PlayListMixin
# Create your views here.

class TaggedItemListView(View):
    def get(self,request):
        tag_list = TaggedItem.object.unique_list()
        context = {
            'tag_list': tag_list,
        }
        return render(request,"tags/tag_list.html",context)

class TaggedItemDetailView(PlayListMixin,ListView):
    """ another ListView for PlayLists """
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = f"{self.kwargs.get('tag')}".title
        return context

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return PlayList.objects.filter(tags__tag=tag).movie_or_show()