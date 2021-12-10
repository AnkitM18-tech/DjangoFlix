"""djangoflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

'''
str -> anything but /
int -> 0 and up
slug -> this-is-slug
uuid -> import uuid ---> uuid.uuid4()
path -> abc/bac/cba
'''

from django.contrib import admin
from django.urls import path
from playlists.views import MovieDetailView, MovieListView,TVShowListView,FeaturedPlayListListView,MovieDetailView,PlayListDetailView,TVShowDetailView,TVShowSeasonDetailView

urlpatterns = [
    path('', FeaturedPlayListListView.as_view()),
    path('admin/', admin.site.urls),
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>/', MovieDetailView.as_view()),
    path('media/<int:pk>/',PlayListDetailView.as_view()),
    path('shows/<slug:showSlug>/seasons/<slug:seasonSlug>/', TVShowSeasonDetailView.as_view()),
    path('shows/<slug:slug>/seasons/', TVShowDetailView.as_view()),
    path('shows/<slug:slug>/', TVShowDetailView.as_view()),
    path('shows/', TVShowListView.as_view()),
]
