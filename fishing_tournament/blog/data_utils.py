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
        koenigsklasse_dict = dict()
        for fish_type, length_border in LENGTH_FILTER_KOENIGSKLASSE.items():
            filtered_query_set = self.posts.filter(fish_type=fish_type, fish_length__gte=length_border)
            if filtered_query_set:
                longest_fish = filtered_query_set.order_by("-fish_length")[0]
                koenigsklasse_dict[fish_type] = longest_fish.fish_length
            else:
                koenigsklasse_dict[fish_type] = "-"
        
        return koenigsklasse_dict
    
    def calc_score(self):
        score = 0
        for fish_type, factor in FISH_FACTOR_KOENIGSKLASSE.items():
            fish_lenght = self.koenigsklasse_dict[fish_type]
            score +=  fish_lenght * factor if isinstance(fish_lenght, float) else 0
        return float(f'{score:.2f}')


class UserScoresRotauge(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.rotaugen = self.get_rotaugen()
        self.score = self.calc_score()

        for i, fish_length in enumerate(self.rotaugen, 1):
            setattr(self, f'Rotauge_{i}', fish_length)
    
    def get_rotaugen(self):
        filtered_query_set = self.posts.filter(fish_type="Rotauge").order_by("-fish_length")
        rotaugen = [routauge.fish_length for routauge in filtered_query_set]
        if(len(rotaugen) > 5):
            rotaugen = rotaugen[:5]
        return rotaugen + ["-"] * (5 - len(rotaugen))

    def calc_score(self):
        score = sum([0 if fish_length=="-" else fish_length for fish_length in self.rotaugen])
        return float(f'{score:.2f}') 


class UserScoresWels(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.score = self.get_wels()
    
    def get_wels(self):
        wels_list = self.posts.filter(fish_type="Wels").order_by("-fish_length")
        longest = wels_list[0].fish_length if wels_list else 0
        return float(f'{longest:.2f}')


class UserScoresBarbe(UserScores):
    def __init__(self, request, user_id, year):
        super().__init__(request, user_id, year)
        self.score = self.get_barbe()
    
    def get_barbe(self):
        barbe_list = self.posts.filter(fish_type="Barbe").order_by("-fish_length")
        longest = barbe_list[0].fish_length if barbe_list else 0
        return float(f'{longest:.2f}')