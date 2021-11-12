from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from .models import Video

class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="This is my title")
        Video.objects.create(title="This is my title",state=Video.VideoStateOptions.PUBLISH)

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        now = timezone.now()
        published_qs = Video.objects.filter(publish_timestamp__lte = now,state=Video.VideoStateOptions.PUBLISH)
        # qs = Video.objects.filter(state=Video.VideoStateOptions.PUBLISH)
        self.assertTrue(published_qs.exists())