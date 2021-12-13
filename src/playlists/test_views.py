from django import test
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from djangoflix.db.models import PublishStateOptions
from .models import PlayList,TVShowProxy,MovieProxy
from videos.models import Video

class PlayListViewTestCase(TestCase):
    fixtures = ['project']

    # def test_queryset_exists(self):
    #     self.assertTrue(PlayList.objects.exists())

    def test_movie_count(self):
        qs = MovieProxy.objects.all()
        self.assertEqual(qs.count(),3)

    def test_show_count(self):
        qs = TVShowProxy.objects.all()
        self.assertEqual(qs.count(),2)

    def test_show_detail_view(self):
        show = TVShowProxy.objects.all().published().first()
        url = show.get_absolute_url()
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,f"{show.title}")
        # html = response.content
        context = response.context
        obj = context['object']
        self.assertEqual(obj.id,show.id)

    def test_show_detail_redirect_view(self):  # not preferred
        show = TVShowProxy.objects.all().published().first()
        url = f"/shows/{show.slug}"
        response = self.client.get(url,follow=True)  # to suppress the 301 error for / follow=True is set
        self.assertEqual(response.status_code,200)

    def test_show_list_view(self):
        shows_qs = TVShowProxy.objects.all().published()
        response = self.client.get("/shows/")
        self.assertEqual(response.status_code,200)
        context = response.context
        res_qs = context['object_list']
        self.assertQuerysetEqual(shows_qs.order_by('-timestamp'),res_qs.order_by('-timestamp'))

    def test_movie_detail_view(self):
        movie = MovieProxy.objects.all().published().first()
        url = movie.get_absolute_url()
        self.assertIsNotNone(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,f"{movie.title}")
        # html = response.content
        context = response.context
        obj = context['object']
        self.assertEqual(obj.id,movie.id)

    def test_movie_detail_redirect_view(self):
        movie = MovieProxy.objects.all().published().first()
        url = f"/movies/{movie.slug}"
        response = self.client.get(url,follow=True)  # to suppress the 301 error for / follow=True is set
        self.assertEqual(response.status_code,200)

    def test_movie_list_view(self):
        movies_qs = MovieProxy.objects.all().published()
        response = self.client.get("/movies/")
        self.assertEqual(response.status_code,200)
        context = response.context
        res_qs = context['object_list']
        self.assertQuerysetEqual(movies_qs.order_by('-timestamp'),res_qs.order_by('-timestamp'))

    def test_search_none_view(self):
        query = None
        response = self.client.get("/search/")
        play_qs = PlayList.objects.none()
        self.assertEqual(response.status_code,200)
        context = response.context
        res_qs = context['object_list']
        self.assertQuerysetEqual(play_qs.order_by('-timestamp'),res_qs.order_by('-timestamp'))
        self.assertContains(response,"Perform a search")

    def test_search_results_view(self):
        query = "Action"
        response = self.client.get(f"/search/?q={query}")
        play_qs = PlayList.objects.all().search(query=query)
        self.assertEqual(response.status_code,200)
        context = response.context
        res_qs = context['object_list']
        self.assertQuerysetEqual(play_qs.order_by('-timestamp'),res_qs.order_by('-timestamp'))
        self.assertContains(response,f"Searched for {query}")