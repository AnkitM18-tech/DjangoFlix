from django import test
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.
from djangoflix.db.models import PublishStateOptions
from .models import PlayList
from videos.models import Video

class PlayListModelTestCase(TestCase):
    def setUp(self):
        video_a = Video.objects.create(title="My Title",video_id="abc123")
        self.video_a = video_a
        self.obj_a = PlayList.objects.create(title="This is my title",video=video_a)
        self.obj_b = PlayList.objects.create(title="This is my title",state=PublishStateOptions.PUBLISH,video=video_a)

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)

    def test_video_playlist(self):
        qs = self.video_a.playlist_set.all()
        self.assertEqual(qs.count(),2)

    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug,self.obj_a.slug)

    def test_valid_title(self):
        title = "This is my title"
        qs = PlayList.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = PlayList.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = PlayList.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        published_qs = PlayList.objects.filter(publish_timestamp__lte = now,state=PublishStateOptions.PUBLISH)
        # qs = PlayList.objects.filter(state=PlayList.PlayListStateOptions.PUBLISH)
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = PlayList.objects.all().published()
        # published_qs_2 = PlayList.objects.published()
        self.assertTrue(published_qs.exists())
        # self.assertEqual(published_qs.count(),published_qs_2.count())