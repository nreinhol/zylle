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

    return user_ids


def get_sum_longest_fishes_of_user(user_id, fish_type, request):
    longest_fish_posts = Post.objects.filter(author=user_id).filter(fish_type=fish_type).order_by('-fish_length')[0:3]
    sum_longest_fishes = sum([post.fish_length for post in longest_fish_posts])

    return sum_longest_fishes


def get_username_of_userid(user_id, request):
    return User.objects.filter(id=user_id)[0].username


def create_data(request, json_format=True):
    barsch_faktor = 2
    zander_faktor = 1.5
    hecht_faktor = 1

    usernames = []

    # real_fish_length
    barsch_data = []
    hecht_data = []
    zander_data = []

    sum_of_each_division = []

    # fish_points
    barsch_point_data = []
    hecht_point_data = []
    zander_point_data = []
    
    # overall data lists
    overall_data = []
    sorted_overall_data = []


    user_ids = get_all_userids_of_posts(request)
    
    for user_id in user_ids:
        usernames.append(get_username_of_userid(user_id, request))
        
        # get sum of longest barsch of user
        user_barsch = get_sum_longest_fishes_of_user(user_id, 'Barsch', request)
        barsch_data.append(user_barsch)

        user_barsch_point = user_barsch*barsch_faktor
        barsch_point_data.append(user_barsch_point)
        
        # get sum of longest hecht of user
        user_hecht = get_sum_longest_fishes_of_user(user_id, 'Hecht', request)
        hecht_data.append(user_hecht)

        user_hecht_point = user_hecht*hecht_faktor
        hecht_point_data.append(user_hecht_point)
        
        # get sum of longest zander of user
        user_zander = get_sum_longest_fishes_of_user(user_id, 'Zander', request)
        zander_data.append(user_zander)

        user_zander_point = user_zander*zander_faktor
        zander_point_data.append(user_zander_point)

        # calc sum of each divison
        sum_of_each_division.append(user_barsch + user_hecht + user_zander)

        # calc overall score of user
        overall_data.append(user_barsch_point + user_hecht_point + user_zander_point)

        # get sorted list of overall points organized in tuples
        sorted_overall_data = sorted(list(zip(usernames, overall_data)), key=lambda tup: tup[1], reverse=True)
        sorted_usernames = [tuple[0] for tuple in sorted_overall_data]
        sorted_points = [tuple[1] for tuple in sorted_overall_data]


    data = {
        'label_data': usernames,
        'barsch_data': barsch_data,
        'hecht_data': hecht_data,
        'zander_data': zander_data,
        'overall_data': overall_data,
        'sorted_usernames': sorted_usernames,
        'sorted_points': sorted_points,
        'sum_of_each_division': sum_of_each_division
    }

    if json_format:
        return JsonResponse(data)
    else:
        return data