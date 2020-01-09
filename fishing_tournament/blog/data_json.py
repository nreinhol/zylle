from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Post
from . import data_utils


def create_chartjs_data(request):
    usernames, overall_sum, overall_score = ([] for i in range(3))
    user_ids = data_utils.get_all_userids_of_posts(request)

    for user_id in user_ids:
        usernames.append(data_utils.get_username_of_userid(request, user_id))
        overall_sum.append(data_utils.get_overall_sum(request, user_id))
        overall_score.append(data_utils.get_overall_score(request, user_id))
    
        # sort overall score data descending
        sorted_overall_data = sorted(list(zip(usernames, overall_score)), key=lambda tup: tup[1], reverse=True)
        sorted_usernames = [tuple[0] for tuple in sorted_overall_data]
        sorted_overall_score = [tuple[1] for tuple in sorted_overall_data]
    
    data = {
        'usernames': usernames,
        'sorted_usernames': sorted_usernames,
        'sorted_overall_score': sorted_overall_score,
        'overall_sum': overall_sum
    }

    return JsonResponse(data)

