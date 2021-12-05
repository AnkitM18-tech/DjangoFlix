from django.test import TestCase
from .models import Category
from playlists.models import PlayList
# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        cat_a = Category.objects.create(title="Action")
        cat_b = Category.objects.create(title="Comedy",active=False)
        self.playlist_a = PlayList.objects.create(title="The Title",category=cat_a)
        self.cat_a = cat_a
        self.cat_b = cat_b

    def test_is_active(self):
        self.assertTrue(self.cat_a.active)

    def test_is_not_active(self):
        self.assertFalse(self.cat_b.active)

    def test_related_playlist(self):
        qs = self.cat_a.playlists.all()
        self.assertEqual(qs.count(),1)