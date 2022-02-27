from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post


# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Homer", password="petriheil", email="homer.simpson@web.de")
        User.objects.create_user(username="Bart", password="petriheil", email="bart.simpson@web.de")

    def test_user_exist(self):
        self.assertEqual(len(list(User.objects.all())), 2)

    def test_user_information(self):
        user = User.objects.get(username="Homer")
        self.assertEqual(user.username, "Homer")
        self.assertEqual(user.email, "homer.simpson@web.de")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.id, 1)

    def test_posts(self):
        Post.objects.create(author_id=1, fish_type="Wels", fish_length=14.6)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, "Homer")
    
        
        