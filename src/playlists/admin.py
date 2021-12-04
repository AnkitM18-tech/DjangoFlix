from django.contrib import admin
from .models import PlayList,PlayListItem,TVShowProxy,TVShowSeasonProxy
# Register your models here.

class SeasonEpisodeInline(admin.TabularInline):
    model=PlayListItem
    extra=0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines=[SeasonEpisodeInline]
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
    inlines = [TVShowSeasonProxyInline]
    list_display = ['title']
    fields = ['title','description','video','slug','state']
    class Meta:
        model = TVShowProxy
    def get_queryset(self,request):
        return TVShowProxy.objects.all()

admin.site.register(TVShowProxy,TVShowProxyAdmin)

class PlayListItemInline(admin.TabularInline):
    model=PlayListItem
    extra=0

class PlayListAdmin(admin.ModelAdmin):
    inlines=[PlayListItemInline]
    class Meta:
        model = PlayList

admin.site.register(PlayList,PlayListAdmin)