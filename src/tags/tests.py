from django.test import TestCase
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
# Create your tests here.
from playlists.models import PlayList
from .models import TaggedItem

class TaggedItemTestCase(TestCase):
    def setUp(self):
        ply_title = "new title"
        self.playlist_obj = PlayList.objects.create(title=ply_title)
        self.playlist_obj2 = PlayList.objects.create(title=ply_title)
        self.ply_title=ply_title
        self.playlist_obj.tags.add(TaggedItem(tag="new-tag"),bulk=False)
        self.playlist_obj2.tags.add(TaggedItem(tag="new-tag"),bulk=False)

    def test_content_type_is_not_null(self):
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag="my-tag")

    def test_create_via_content_type(self):
        c_type = ContentType.objects.get(app_label="playlists",model="playlist")
        #c_type.model_class()
        tag_a = TaggedItem.objects.create(content_type=c_type,object_id=1,tag='new-tag')
        self.assertIsNotNone(tag_a.pk)
        tag_b = TaggedItem.objects.create(content_type=c_type,object_id=2,tag='new-tag2')
        self.assertIsNotNone(tag_b.pk)

    def test_create_via_model_content_type(self):
        c_type = ContentType.objects.get_for_model(PlayList)
        tag_a = TaggedItem.objects.create(content_type=c_type,object_id=1,tag='new-tag')
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_app_loader_content_type(self):
        PlayListKlass = apps.get_model(app_label="playlists",model_name="PlayList")
        c_type = ContentType.objects.get_for_model(PlayListKlass)
        tag_a = TaggedItem.objects.create(content_type=c_type,object_id=1,tag='new-tag')
        self.assertIsNotNone(tag_a.pk)

    def test_related_field(self):
        self.assertEqual(self.playlist_obj.tags.count(),1)

    def test_related_field_create(self):
        self.playlist_obj.tags.create(tag="another-tag")
        self.assertEqual(self.playlist_obj.tags.count(),2)

    def test_related_field_query_name(self):
        qs = TaggedItem.objects.filter(playlist__title__iexact=self.ply_title)
        self.assertEqual(qs.count(),2)

    def test_related_field_via_content_type(self):
        c_type = ContentType.objects.get_for_model(PlayList)
        tag_qs = TaggedItem.objects.filter(content_type=c_type,object_id=self.playlist_obj.id)
        self.assertEqual(tag_qs.count(),1)

    def test_direct_object_creation(self):
        obj = self.playlist_obj
        tag =TaggedItem.objects.create(content_object=obj,tag="another-one")
        self.assertIsNotNone(tag.pk)