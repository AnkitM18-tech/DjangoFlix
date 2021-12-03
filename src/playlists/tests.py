from django import test
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
# Create your tests here.
from djangoflix.db.models import PublishStateOptions
from .models import PlayList
from videos.models import Video

class PlayListModelTestCase(TestCase):
    def create_videos(self):
        video_a = Video.objects.create(title="My Title",video_id="abc123")
        video_b = Video.objects.create(title="My Title",video_id="abc1234")
        video_c = Video.objects.create(title="My Title",video_id="abc12345")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        self.video_qs = Video.objects.all()

    def setUp(self):
        self.create_videos()
        self.obj_a = PlayList.objects.create(title="This is my title",video=self.video_a)
        obj_b = PlayList.objects.create(title="This is my title",state=PublishStateOptions.PUBLISH,video=self.video_a)
        # obj_b.videos.set([self.video_a,self.video_b,self.video_c])
        obj_b.videos.set(self.video_qs)
        obj_b.save()
        self.obj_b = obj_b

    def test_playlist_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)

    def test_playlist_video_items(self):
        count = self.obj_b.videos.all().count()
        self.assertEqual(count,3)

    def test_playlist_video_through_model(self):
        video_qs =sorted(list(self.video_qs.values_list('id')))
        playlist_obj_video_qs =sorted(list( self.obj_b.videos.all().values_list('id')))
        playlist_obj_playlist_item_qs =sorted(list( self.obj_b.playlistitem_set.all().values_list('video')))
        self.assertEqual(video_qs,playlist_obj_video_qs,playlist_obj_playlist_item_qs)

    def test_video_playlist_property(self):
        ids = self.obj_a.video.get_playlist_ids()
        actual_ids = list(PlayList.objects.filter(video=self.video_a).values_list('id',flat=True))
        self.assertEqual(ids,actual_ids)

    def test_video_playlist(self):
        qs = self.video_a.playlist_featured.all()
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