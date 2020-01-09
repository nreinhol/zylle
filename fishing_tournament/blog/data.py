from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Post

from . import data_utils

def get_user_data_container(request):
    user_ids = data_utils.get_all_userids_of_posts(request)

    return [UserDataContainer(request, user_id) for user_id in user_ids]
    


class UserDataContainer(object):
    def __init__(self, request, user_id):
        self.username = data_utils.get_username_of_userid(request, user_id)
        self.longest_barsch = data_utils.get_beautified_three_longest_fishes(request, user_id, 'Barsch')
        self.longest_hecht = data_utils.get_beautified_three_longest_fishes(request, user_id, 'Hecht')
        self.longest_zander = data_utils.get_beautified_three_longest_fishes(request, user_id, 'Zander')


