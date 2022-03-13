import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from . import data_utils


def get_user_scores(request, class_object, year=data_utils.COMPETITION_YEAR):
    user_ids = data_utils.get_all_user_ids(request)
    sorted_user_scores = sorted([class_object(request, user_id, year) for user_id in user_ids], reverse=True)
    data_utils.set_positions(sorted_user_scores)
    return sorted_user_scores


def get_user_scores_koenigsklasse(request):
    return get_user_scores(request, data_utils.UserScoresKoenigsklasse)


def get_user_scores_rotauge(request):
    return get_user_scores(request, data_utils.UserScoresRotauge)


def get_user_scores_wels(request):
    return get_user_scores(request, data_utils.UserScoresWels)


def get_user_scores_barbe(request):
    return get_user_scores(request, data_utils.UserScoresBarbe)