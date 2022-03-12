from django.contrib.auth.models import User
from datetime import timezone
import json

from .models import Post

COMPETITION_YEAR = 2022

FISH_FACTOR_KOENIGSKLASSE = {
    "Barsch": 2.4,
    "Hecht": 1,
    "Zander": 1.4,
    "Karpfen": 1,
    "Schleie": 2.4
}

LENGTH_FILTER_KOENIGSKLASSE = {
    "Barsch": 25,
    "Hecht": 60,
    "Zander": 50,
    "Karpfen": 50,
    "Schleie": 40
}


def get_all_user_ids(request):
    user_ids = [user.id for user in User.objects.all()]
    if len(user_ids) > 1:
        del user_ids[0]
        return user_ids
    else:
        return list()


def set_positions(sorted_user_scores):
    for i, UserScoresKoenigsklasse in enumerate(sorted_user_scores, 1):
        UserScoresKoenigsklasse.position = f'{i}.'


class UserData(object):
    def __init__(self, request, user_id, year):
        self.username = User.objects.filter(id=user_id)[0].username
        self.year = year
        self.posts = Post.objects.filter(date_posted__year=year, author_id=user_id)


class UserScoresKoenigsklasse(UserData):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.fish_dict = self.get_fish_dict(request, self.posts)
        self.score = self.calc_score(request)
        self.position = None

        for fish_type, fish_length in self.fish_dict.items():
            setattr(self, fish_type, fish_length)

    def __lt__(self, other):
        return self.score < other.score

    def get_fish_dict(self, request, post_list):
        fish_dict = dict()
        for fish_type, length_border in LENGTH_FILTER_KOENIGSKLASSE.items():
            filtered_query_set = post_list.filter(fish_type=fish_type, fish_length__gte=length_border)
            if filtered_query_set:
                longest_fish = filtered_query_set.order_by("-fish_length")[0]
                fish_dict[fish_type] = longest_fish.fish_length
            else:
                fish_dict[fish_type] = "-"
        
        return fish_dict
    
    def calc_score(self, request):
        score = 0
        for fish_type, factor in FISH_FACTOR_KOENIGSKLASSE.items():
            fish_lenght = self.fish_dict[fish_type]
            score +=  fish_lenght * factor if isinstance(fish_lenght, float) else 0
        return score