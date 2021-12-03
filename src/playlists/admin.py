from django.contrib import admin
from .models import PlayList,PlayListItem
# Register your models here.
class PlayListItemInline(admin.TabularInline):
    model=PlayListItem
    extra=0
class PlayListAdmin(admin.ModelAdmin):
    inlines=[PlayListItemInline]
    class Meta:
        model = PlayList
admin.site.register(PlayList,PlayListAdmin)