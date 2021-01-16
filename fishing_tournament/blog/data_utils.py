from django.contrib.auth.models import User

from .models import Post


FISH_TYPES = ['Barsch', 'Hecht', 'Zander']
FISH_DICT = {'Barsch': 2, 'Hecht': 1, 'Zander': 1.3}


def get_all_userids_of_posts(request):
    '''Returns a list containing all distinct userids from postlist'''
    user_ids_tuple = list(Post.objects.values_list('author').distinct())
    return [ids_tuple[0] for ids_tuple in user_ids_tuple]


def get_username_of_userid(request, user_id):
    return User.objects.filter(id=user_id)[0].username


def get_three_longest_fishes(request, user_id, fish_type):
    return Post.objects.filter(author=user_id).filter(fish_type=fish_type).filter(date_posted__year="2021").order_by('-fish_length')[0:3]


def get_beautified_three_longest_fishes(request, user_id, fish_type):
    three_longest_fishes = get_three_longest_fishes(request, user_id, fish_type)
    fish_lengths = [fish.fish_length for fish in three_longest_fishes]
    no_entry = ['-'] * 3
    beautified_fish_lengths = fish_lengths + no_entry

    return beautified_fish_lengths[0:3]



def get_sum_of_fish_type(request, user_id, fish_type):
    '''Returns the sum of the three longest fishes of a given fish type'''
    three_longest_fishes = get_three_longest_fishes(request, user_id, fish_type)
    return sum([fish.fish_length for fish in three_longest_fishes])


def get_overall_sum(request, user_id):
    '''Returns the sum of the sum of the three longest fishes for each fish type'''
    return sum([get_sum_of_fish_type(request, user_id, key) for key in FISH_DICT])


def get_overall_score(request, user_id):
    '''Returns the sum of the sum of the three longest fishes for each fish type multiplied by his factors'''
    return sum([get_sum_of_fish_type(request, user_id, key) * FISH_DICT[key] for key in FISH_DICT])
