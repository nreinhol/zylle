from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Post


def get_dummy_data(request):

    data = {
        'label_data': ['Fredi', 'Gesi', 'Olli'],
        'barsch_data': [360, 389, 325],
        'hecht_data': [230, 390, 410],
    }

    return JsonResponse(data)


def get_all_userids_of_posts(request):
    user_ids_tuple = list(Post.objects.values_list('author').distinct())
    user_ids = [ids_tuple[0] for ids_tuple in user_ids_tuple]
    
    # remove admin because should not displayed in charts 
    del user_ids[0]

    return user_ids


def get_sum_longest_fishes_of_user(user_id, fish_type, request):
    longest_fish_posts = Post.objects.filter(author=user_id).filter(fish_type=fish_type).order_by('-fish_length')[0:3]
    sum_longest_fishes = sum([post.fish_length for post in longest_fish_posts])

    return sum_longest_fishes


def get_username_of_userid(user_id, request):
    return User.objects.filter(id=user_id)[0].username


def create_data(request):
    usernames = []
    barsch_data = []
    hecht_data = []
    zander_data = []
    overall_data = []

    user_ids = get_all_userids_of_posts(request)
    
    for user_id in user_ids:
        usernames.append(get_username_of_userid(user_id, request))
        
        # get sum of longest barsch of user
        user_barsch = get_sum_longest_fishes_of_user(user_id, 'Barsch', request)
        barsch_data.append(user_barsch)
        
        # get sum of longest hecht of user
        user_hecht = get_sum_longest_fishes_of_user(user_id, 'Hecht', request)
        hecht_data.append(user_hecht)
        
        # get sum of longest zander of user
        user_zander = get_sum_longest_fishes_of_user(user_id, 'Zander', request)
        zander_data.append(user_zander)

        # calc overall score of user
        overall_data.append(user_barsch + user_hecht + user_zander)


    data = {
        'label_data': usernames,
        'barsch_data': barsch_data,
        'hecht_data': hecht_data,
        'zander_data': zander_data,
        'overall_data': overall_data
    }

    return JsonResponse(data)