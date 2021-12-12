class PlayListMixin():
    title = None
    template_name = "playlist_list.html"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context["title"] = self.title
        # print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().published()