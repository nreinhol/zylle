from django.contrib.auth.models import User
from datetime import timezone
from enum import Enum
import json

from .models import Post

COMPETITION_YEAR = 2023


class Fishes(Enum):
    Barsch = 2.4, 25
    Hecht = 1, 60
    Zander = 1.4, 50
    Rapfen = 1, 45
    
    def __init__(self, factor, bound):
        self.factor = factor
        self.bound = bound


def get_all_user_ids(request):
    user_ids = list()
    for user in User.objects.all():
        if user.is_active and user.id != 1:
            user_ids.append(user.id)
    return user_ids


def set_positions(sorted_user_scores):
    for i, UserScoresKoenigsklasse in enumerate(sorted_user_scores, 1):
        UserScoresKoenigsklasse.position = f'{i}.'


class UserScores(object):
    def __init__(self, request, user_id, year):
        self.user_id = user_id
        self.img = User.objects.filter(id=self.user_id)[0].profile.image
        self.username = User.objects.filter(id=self.user_id)[0].username
        self.year = year
        self.posts = Post.objects.filter(date_posted__year=year, author_id=self.user_id)
        self.position = None
        self.score = 0
    
    def __lt__(self, other):
        return self.score < other.score


class UserScoresKoenigsklasse(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.koenigsklasse_dict = self.get_koenigsklasse_dict()
        self.score = self.calc_score()
        
        for fish_type, fish_length in self.koenigsklasse_dict.items():
            setattr(self, fish_type, fish_length)

    def get_koenigsklasse_dict(self):
        keys = ["1_Barsch", "2_Barsch", "3_Barsch", "1_Hecht", "2_Hecht", "3_Hecht", "1_Zander", "2_Zander", "3_Zander", "Rapfen"]
        koenigsklasse_dict = {**dict.fromkeys(keys, "-")}
        for fish in Fishes:
            filtered_query_set = self.posts.filter(fish_type=fish.name, fish_length__gte=fish.bound)
            if filtered_query_set:
                if fish is Fishes.Rapfen:
                    koenigsklasse_dict[fish.name] = filtered_query_set.order_by("-fish_length")[0].fish_length
                else:
                    for i, entry in enumerate(filtered_query_set.order_by("-fish_length")[:3], 1):
                        key = f"{i}_{fish.name}"
                        koenigsklasse_dict[key] = entry.fish_length 
        return koenigsklasse_dict                 


    def calc_score(self):
        score = 0
        for fish in Fishes:
            if fish is not Fishes.Rapfen:
                for i in range(3):
                    key = f"{i+1}_{fish.name}"
                    length = self.koenigsklasse_dict[key]
                    score += length * fish.factor if isinstance(length, float) else 0
            else:
                length = self.koenigsklasse_dict[fish.name]
                score +=  length * fish.factor if isinstance(length, float) else 0

        return float(f'{score:.2f}')


class UserScoresSchleie(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.fishes = self.get_fishes()
        self.score = self.calc_score()
    
    def get_fishes(self):
        filtered_query_set = self.posts.filter(fish_type="Schleie", fish_length__gte=40).order_by("-fish_length")[:3]
        fish_list = [query_entry.fish_length for query_entry in filtered_query_set]
        fish_list = fish_list + [0] * (3 - len(fish_list))  # fill with zeros
        return fish_list

        
    def calc_score(self):
        score = sum(self.fishes)
        return float(f'{score:.2f}')


class UserScoresKarpfen(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.fishes = self.get_fishes()
        self.score = self.calc_score()
    
    def get_fishes(self):
        filtered_query_set = self.posts.filter(fish_type="Karpfen", fish_length__gte=50).order_by("-fish_length")
        fish_list = [query_entry.fish_length for query_entry in filtered_query_set]
        fish_list = fish_list + [0] * (3 - len(fish_list))  # fill with zeros
        return fish_list
    
    def calc_score(self):
        score = sum(self.fishes)
        return float(f'{score:.2f}')
