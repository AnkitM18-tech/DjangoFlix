from django.test import TestCase
from django.contrib.auth import get_user_model
import random
from playlists.models import PlayList
from .models import Rating,RatingChoices
# Create your tests here.

User = get_user_model()  #User.objects.all()

class RatingTestCases(TestCase):

    def create_playlists(self):
        self.playlist_count = random.randint(1,10)
        items=[]
        for i in range(0,self.playlist_count):
            items.append(PlayList(title=f"TVS_{i}"))
        PlayList.objects.bulk_create(items)
        self.playlists = PlayList.objects.all()

    def create_users(self):
        self.user_count = random.randint(1,10)
        items=[]
        for i in range(0,self.user_count):
            items.append(User(username=f"user_{i}"))
        User.objects.bulk_create(items)
        self.users = User.objects.all()
    
    def create_ratings(self):
        self.rating_count = 1_000
        items=[]
        for i in range(0,self.rating_count):
            user_obj = self.users.order_by('?').first()  #random order
            ply_obj = self.playlists.order_by('?').first()
            items.append(Rating(user=user_obj,content_object=ply_obj,value=random.choice(RatingChoices.choices)[0]))  #getting first tuple value
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()

    def setUp(self):
        self.create_users()
        self.create_playlists()
        self.create_ratings()

    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.user_count)
        self.assertEqual(self.users.count(),self.user_count)

    def test_playlist_count(self):
        qs = PlayList.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.playlist_count)
        self.assertEqual(self.playlists.count(),self.playlist_count)

    def test_rating_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.rating_count)
        self.assertEqual(self.ratings.count(),self.rating_count)

    def test_rating_random_choices(self):
        value_set =set(Rating.objects.values_list("value",flat=True))
        self.assertTrue(len(value_set)>1)