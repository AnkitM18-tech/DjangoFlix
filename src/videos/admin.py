from django.contrib import admin

# Register your models here.
from .models import VideoAllProxy,VideoPublishedProxy

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title','video_id']
    search_fileds = ['title']
    # list_filter = ['video_id']
    class Meta:
        model = VideoAllProxy

admin.site.register(VideoAllProxy,VideoAllAdmin)

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title','video_id']
    search_fileds = ['title']
    # list_filter = ['video_id']
    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self,request):
        return VideoAllProxy.objects.filter(active=True)

admin.site.register(VideoPublishedProxy,VideoPublishedProxyAdmin)