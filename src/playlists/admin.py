from django.contrib import admin
from .models import PlayList,PlayListItem,TVShowProxy,TVShowSeasonProxy,MovieProxy,PlayListRelated
from tags.admin import TaggedItemInLine
# Register your models here.

class MovieProxyAdmin(admin.ModelAdmin):
    inlines=[TaggedItemInLine]
    list_display = ['title']
    fields = ['title','description','video','category','slug','state']
    class Meta:
        model = MovieProxy

    def get_queryset(self, request):
        return MovieProxy.objects.all()

admin.site.register(MovieProxy,MovieProxyAdmin)

class SeasonEpisodeInline(admin.TabularInline):
    model=PlayListItem
    extra=0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines=[TaggedItemInLine,SeasonEpisodeInline]
    list_display = ['title','parent']
    class Meta:
        model = TVShowSeasonProxy

    def get_queryset(self,request):
        return TVShowSeasonProxy.objects.all()

admin.site.register(TVShowSeasonProxy,TVShowSeasonProxyAdmin)

class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order','title','state']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInLine,TVShowSeasonProxyInline]
    list_display = ['title']
    fields = ['title','description','video','category','slug','state']
    class Meta:
        model = TVShowProxy
    def get_queryset(self,request):
        return TVShowProxy.objects.all()

admin.site.register(TVShowProxy,TVShowProxyAdmin)

class PlayListRelatedInLine(admin.TabularInline):
    model = PlayListRelated
    fk_name = 'playlist'
    extra = 0


class PlayListItemInline(admin.TabularInline):
    model=PlayListItem
    extra=0

class PlayListAdmin(admin.ModelAdmin):
    inlines=[PlayListRelatedInLine,PlayListItemInline,TaggedItemInLine]
    fields=[
        'title','description','slug','state','active'
    ]
    class Meta:
        model = PlayList

    def get_queryset(self, request):
        return PlayList.objects.filter(type=PlayList.PlayListTypeChoices.PLAYLIST)

admin.site.register(PlayList,PlayListAdmin)