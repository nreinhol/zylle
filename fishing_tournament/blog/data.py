import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from . import data_utils


def get_user_scores_koenigsklasse(request, year=data_utils.COMPETITION_YEAR):
    user_ids = data_utils.get_all_user_ids(request)
    sorted_user_scores = sorted([data_utils.UserScoresKoenigsklasse(request, user_id, year) for user_id in user_ids], reverse=True)
    data_utils.set_positions(sorted_user_scores)
    return sorted_user_scores
    
