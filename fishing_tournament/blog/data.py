import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

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


class RankingList(object):
    def __init__(self, request):
        self.ranking = data_utils.get_ranking_list(request)
        self.usernames = json.dumps(self.ranking["usernames"])
        self.scores = json.dumps(self.ranking["scores"])


class UserStatistics(object):
    def __init__(self, request, user_id):
        self.amount_barsch = len(data_utils.get_all_fishes_of_fish_type(request, user_id, 'Barsch'))
        self.amount_hecht = len(data_utils.get_all_fishes_of_fish_type(request, user_id, 'Hecht'))
        self.amount_zander = len(data_utils.get_all_fishes_of_fish_type(request, user_id, 'Zander'))
        self.total_amount_fishes = data_utils.get_amount_all_fishes_of_user(request, user_id)
        self.longest_fish = data_utils.get_longest_fish_of_user(request, user_id)