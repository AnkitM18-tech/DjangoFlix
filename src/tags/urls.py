from django.urls import path
from .views import TaggedItemListView,TaggedItemDetailView
urlpatterns = [
    path('',TaggedItemListView.as_view()),
    path('<slug:tag>/',TaggedItemDetailView.as_view()),
]
