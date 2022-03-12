from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from .models import Post

from . import data_utils


# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Homer", password="petriheil", email="homer.simpson@web.de")
        User.objects.create_user(username="Bart", password="petriheil", email="bart.simpson@web.de")
        Post.objects.create(author_id=1, fish_type="Wels", fish_length=14.6)
        Post.objects.create(author_id=1, fish_type="Barsch", fish_length=20.8)
        Post.objects.create(author_id=1, fish_type="Zander", fish_length=30.3)
        Post.objects.create(author_id=1, fish_type="Zander", fish_length=60.37)
        Post.objects.create(author_id=1, fish_type="Schleie", fish_length=45.7)
        Post.objects.create(author_id=1, fish_type="Schleie", fish_length=35.7)
    
    def test_user_exist(self):
        self.assertEqual(len(list(User.objects.all())), 2)

    def test_user_information(self):
        user = User.objects.get(username="Homer")
        self.assertEqual(user.username, "Homer")
        self.assertEqual(user.email, "homer.simpson@web.de")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.id, 1)

    def test_posts(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, "Homer")
    
    def test_get_all_posts_of_user(self):
        self.assertEqual(len(list(Post.objects.filter(date_posted__year=2022, author_id=1))), 6)

    def test_filter_posts(self):
        koenigsklasse_dict = {}
        for fish_type, length_border in data_utils.LENGTH_FILTER_KOENIGSKLASSE.items():
            filtered_query_set = Post.objects.all().filter(fish_type=fish_type, fish_length__gte=length_border)
            if filtered_query_set:
                longest_fish = filtered_query_set.order_by("-fish_length")[0]
                koenigsklasse_dict[fish_type] = longest_fish.fish_length
            else:
                koenigsklasse_dict[fish_type] = "-"
        
        print(koenigsklasse_dict)

        
        
        